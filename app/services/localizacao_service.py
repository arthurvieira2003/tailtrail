def process_data(latitude: float, longitude: float) -> bool:

    if (latitude is None or longitude is None):
        raise Exception("Latitude e longitude não podem ser nulos.")
    
    print(f"Processando dados: Latitude = {latitude}, Longitude = {longitude}")

    return True
