import os
import requests
import json
from datetime import datetime
import time

# Configurações
DOCKERHUB_USERNAME = os.getenv("DOCKERHUB_USERNAME")
DOCKERHUB_PASSWORD = os.getenv("DOCKERHUB_PASSWORD")
IMAGE_NAME = "tailtrail"
IMAGE_TAG = datetime.now().strftime("%Y%m%d_%H%M%S")

PORTAINER_URL = os.getenv("PORTAINER_URL")
PORTAINER_USERNAME = os.getenv("PORTAINER_USERNAME")
PORTAINER_PASSWORD = os.getenv("PORTAINER_PASSWORD")
ENDPOINT_ID = "2"  # Definindo um valor padrão para ENDPOINT_ID

def build_and_push_docker():
    # Build da imagem
    build_cmd = f"docker build -t {DOCKERHUB_USERNAME}/{IMAGE_NAME}:{IMAGE_TAG} ."
    if os.system(build_cmd) != 0:
        raise Exception("Erro ao fazer build da imagem Docker")

    # Login no DockerHub
    login_cmd = f"docker login -u {DOCKERHUB_USERNAME} -p {DOCKERHUB_PASSWORD}"
    if os.system(login_cmd) != 0:
        raise Exception("Erro ao fazer login no DockerHub")

    # Push da imagem
    push_cmd = f"docker push {DOCKERHUB_USERNAME}/{IMAGE_NAME}:{IMAGE_TAG}"
    if os.system(push_cmd) != 0:
        raise Exception("Erro ao fazer push da imagem")

def deploy_to_portainer():
    portainer_api_url = f"{PORTAINER_URL}/api"
    
    # Autenticação no Portainer
    auth_url = f"{portainer_api_url}/auth"
    auth_data = {
        "username": PORTAINER_USERNAME,
        "password": PORTAINER_PASSWORD
    }
    
    auth_response = requests.post(auth_url, json=auth_data, verify=False)
    if auth_response.status_code != 200:
        raise Exception(f"Erro na autenticação do Portainer: {auth_response.text}")
    
    jwt_token = auth_response.json()["jwt"]
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    try:
        # Lista todos os containers
        list_containers_url = f"{portainer_api_url}/endpoints/{ENDPOINT_ID}/docker/containers/json?all=true"
        containers = requests.get(list_containers_url, headers=headers, verify=False).json()
        
        container_name = "tail-trail-app"
        existing_container = next((c for c in containers if f"/{container_name}" in c["Names"]), None)
        
        if existing_container:
            container_id = existing_container["Id"]
            
            # Força a parada do container
            print(f"Forçando parada do container {container_id[:12]}...")
            stop_url = f"{portainer_api_url}/endpoints/{ENDPOINT_ID}/docker/containers/{container_id}/stop?t=0"
            requests.post(stop_url, headers=headers, verify=False)
            
            # Aguarda um momento para garantir que o container parou
            time.sleep(2)
            
            # Remove o container com força
            print(f"Removendo container antigo {container_id[:12]}...")
            remove_url = f"{portainer_api_url}/endpoints/{ENDPOINT_ID}/docker/containers/{container_id}?force=true"
            remove_response = requests.delete(remove_url, headers=headers, verify=False)
            
            if remove_response.status_code not in [204, 404]:
                raise Exception(f"Erro ao remover container: {remove_response.text}")
            
            # Aguarda mais um momento após a remoção
            time.sleep(2)

        # Configuração para pull da imagem
        image_name = f"{DOCKERHUB_USERNAME}/{IMAGE_NAME}:{IMAGE_TAG}"
        
        # Pull da nova imagem
        print("Baixando nova imagem...")
        pull_url = f"{portainer_api_url}/endpoints/{ENDPOINT_ID}/docker/images/create?fromImage={image_name}"
        pull_response = requests.post(pull_url, headers=headers, verify=False)
        if pull_response.status_code not in [200, 201]:
            raise Exception(f"Erro ao fazer pull da imagem: {pull_response.text}")
        print("Nova imagem baixada com sucesso.")

        # Configuração do novo container
        container_config = {
            "name": container_name,
            "Image": image_name,
            "HostConfig": {
                "PortBindings": {
                    "7070/tcp": [{"HostPort": "7070"}]
                },
                "RestartPolicy": {
                    "Name": "always"
                }
            },
            "ExposedPorts": {
                "7070/tcp": {}
            }
        }

        # Cria o novo container
        print("Criando novo container...")
        deploy_url = f"{portainer_api_url}/endpoints/{ENDPOINT_ID}/docker/containers/create"
        deploy_response = requests.post(deploy_url, headers=headers, json=container_config, verify=False)
        
        if deploy_response.status_code not in [200, 201]:
            raise Exception(f"Erro ao criar container: {deploy_response.text}")

        # Inicia o novo container
        container_id = deploy_response.json()["Id"]
        print(f"Iniciando novo container {container_id[:12]}...")
        start_url = f"{portainer_api_url}/endpoints/{ENDPOINT_ID}/docker/containers/{container_id}/start"
        start_response = requests.post(start_url, headers=headers, verify=False)
        
        if start_response.status_code not in [204, 200]:
            raise Exception(f"Erro ao iniciar o container: {start_response.text}")
        
        print("Deploy concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante o deploy: {str(e)}")
        raise

def main():
    try:
        print("Iniciando processo de deploy...")
        build_and_push_docker()
        print("Imagem enviada para o DockerHub com sucesso!")
        deploy_to_portainer()
        print("Deploy realizado com sucesso!")
    except Exception as e:
        print(f"Erro durante o deploy: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()