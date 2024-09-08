# Tail Trail: Sistema Inteligente de Rastreamento de Animais de Estimação

## Descrição do Projeto

O **Tail Trail** é um sistema inteligente de rastreamento de animais de estimação, desenvolvido para solucionar problemas como a perda de animais e o monitoramento remoto. Ele combina tecnologias de **Internet das Coisas (IoT)** e **Inteligência Artificial (IA)**, fornecendo aos donos uma maneira prática e eficaz de cuidar e monitorar seus pets.

## Problemas que o Sistema Resolve

- Perda de animais de estimação.
- Monitoramento de comportamento em tempo real.
- Dificuldade de localizar o animal em caso de fuga.

## Objetivos

- Fornecer uma solução integrada para o monitoramento e cuidado de animais de estimação.
- Melhorar a segurança e o bem-estar dos pets com uma plataforma de fácil uso e monitoramento em tempo real.

## Funcionalidades

### Requisitos Funcionais (RF)

1. **Rastreamento em Tempo Real**: Localização precisa do animal usando GPS.
2. **Monitoramento de Comportamento**: Análise de padrões de comportamento e alerta para atividades incomuns.
3. **Integração com Aplicativo Móvel**: Exibição de dados de localização e comportamento.
4. **Notificações e Alertas**: Notificações quando o animal sair de uma área designada ou apresentar comportamento anômalo.
5. **Transmissão de Dados para a Nuvem**: Armazenamento e análise de dados em tempo real.
6. **Comunicação com Plataforma Central**: Envio de dados do microcontrolador para a plataforma via Wi-Fi.

### Requisitos Não Funcionais (RNF)

1. **Precisão do GPS**: Rastreamento preciso em diferentes condições ambientais.
2. **Autonomia da Bateria**: Otimização de energia para garantir duração prolongada da bateria.
3. **Segurança e Privacidade**: Proteção dos dados sensíveis do animal e do dono.
4. **Conectividade Confiável**: Transmissão de dados estável em diferentes locais.
5. **Interface Intuitiva**: Aplicativo móvel fácil de usar para monitorar o pet.
6. **Manutenção e Atualizações**: Facilitar atualizações de software e manutenção do sistema.

## Arquitetura do Projeto

### Componentes de Hardware

1. **Sensor GPS**: Responsável pelo rastreamento da localização do animal. Um exemplo recomendado seria o **NEO-6M GPS Module**, que oferece precisão adequada e fácil integração com microcontroladores.
2. **Microcontrolador**: Gerencia a leitura dos dados do GPS e a comunicação com outros componentes. O **ESP32** é recomendado por sua conectividade Wi-Fi integrada e capacidade de processamento, além de ser de baixo consumo energético.
3. **Módulo de Comunicação (Wi-Fi)**: Permite a transmissão dos dados do microcontrolador para a nuvem ou o aplicativo móvel. O próprio **ESP32** já possui Wi-Fi embutido, mas o **ESP8266** pode ser uma opção caso seja necessário um módulo adicional ou independente.
4. **Fonte de Energia (Bateria)**: Utilizar uma bateria recarregável de **LiPo 3.7V**, que fornece energia suficiente com baixo peso e tamanho compacto, ideal para dispositivos portáteis.

### Componentes de Software

- **Aplicativo Móvel**: O aplicativo será desenvolvido utilizando o **Flutter**, uma plataforma de código aberto para criação de apps multiplataforma (iOS e Android), permitindo uma interface intuitiva e responsiva.
- **Plataforma na Nuvem**: A infraestrutura na nuvem será fornecida pelo **Google Cloud**, oferecendo escalabilidade, armazenamento seguro e serviços de processamento de dados.
- **Algoritmos de IA**: Desenvolvidos em **Python**, os algoritmos analisarão padrões de movimento e comportamento, identificando comportamentos anormais do animal.

## Desafios Antecipados

- **Precisão do GPS**: Garantir rastreamento eficiente em diferentes condições.
- **Gerenciamento de Energia**: Manter autonomia de bateria suficiente para operação prolongada.
- **Conectividade**: Garantir comunicação estável em diferentes locais, mesmo com cobertura limitada.
- **Desenvolvimento da IA**: Criar modelos de IA precisos para análise de comportamento.
- **Segurança e Privacidade**: Proteger dados sensíveis dos usuários e dos animais.
- **Desenvolvimento do Aplicativo**: Criar uma interface intuitiva e responsiva para o usuário final.
