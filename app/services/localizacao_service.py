from fastapi import HTTPException
from app.Messaging.Requests.GPSData import GPSData  
import math
from typing import List, Dict, Any
from pydantic import BaseModel
import numpy as np
from scipy.stats import zscore
from fastapi.encoders import jsonable_encoder

class GPSSafetyProcessor:
    def __init__(self, 
                 max_speed_threshold: float = 100,  # km/h 
                 max_distance_threshold: float = 500,  # metros
                 teleportation_threshold: float = 10000  # 10 km
                ):
        """
        Inicializa o processador de segurança de caminho GPS
        :param max_speed_threshold: Velocidade máxima permitida em km/h
        :param max_distance_threshold: Distância máxima entre pontos consecutivos em metros
        :param teleportation_threshold: Distância que caracteriza um salto geográfico
        """
        self.max_speed_threshold = max_speed_threshold
        self.max_distance_threshold = max_distance_threshold
        self.teleportation_threshold = teleportation_threshold

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula distância entre dois pontos GPS usando fórmula de Haversine
        :return: Distância em metros
        """
        R = 6371000  # Raio da Terra em metros
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

    def calculate_path_metrics(self, path: List[GPSData]) -> Dict[str, Any]:
        """
        Calcula métricas de segurança para o caminho
        :param path: Lista de pontos GPS
        :return: Dicionário com métricas de segurança
        """
        if len(path) < 2:
            return {
                "is_safe": True,
                "metrics": {}
            }

        # Inicializa métricas
        metrics = {
            "total_distance": 0,
            "speeds": [],
            "distances": [],
            "safety_flags": {
                "speed_exceeded": False,
                "distance_anomaly": False,
                "teleportation_detected": False
            }
        }

        # Processamento sequencial dos pontos
        for i in range(1, len(path)):
            prev = path[i-1]
            curr = path[i]

            # Calcula distância entre pontos consecutivos
            distance = self.haversine_distance(
                prev.latitude, prev.longitude, 
                curr.latitude, curr.longitude
            )
            metrics["distances"].append(distance)
            metrics["total_distance"] += distance

            # Calcula velocidade (assumindo 1 minuto entre pontos)
            speed_ms = distance / 60  # metros por segundo
            speed_kmh = speed_ms * 3.6  # conversão para km/h
            metrics["speeds"].append(speed_kmh)

            # Verifica limites de segurança
            if speed_kmh > self.max_speed_threshold:
                metrics["safety_flags"]["speed_exceeded"] = True

            if distance > self.max_distance_threshold:
                metrics["safety_flags"]["distance_anomaly"] = True

            if distance > self.teleportation_threshold:
                metrics["safety_flags"]["teleportation_detected"] = True

        return {
            "is_safe": not any(metrics["safety_flags"].values()),
            "metrics": metrics
        }

    def process_data(self, path: List[GPSData]) -> Dict[str, Any]:
        """
        Processa caminho GPS com validações de segurança
        :return: Relatório detalhado de segurança
        """
        try:
            # Validações básicas
            for gps_data in path:
                if gps_data.latitude is None or gps_data.longitude is None:
                    raise ValueError(f"Latitude e longitude não podem ser nulos")

            # Analisa caminho
            path_analysis = self.calculate_path_metrics(path)

            return {
                "processed": True,
                "is_safe": path_analysis["is_safe"],
                "total_points": len(path),
                "total_distance": path_analysis["metrics"].get("total_distance", 0),
                "speeds": path_analysis["metrics"].get("speeds", []),
                "safety_flags": path_analysis["metrics"].get("safety_flags", {})
            }
        
        except Exception as e:
            print(f"Erro ao processar dados: {e}")
            return {
                "processed": False,
                "error": str(e)
            }

def process_data(path: List[GPSData]) -> Dict[str, Any]:
    try:
        processor = GPSSafetyProcessor()
        result = processor.process_data(path)
        return jsonable_encoder(result)
    except HTTPException as e:
        return jsonable_encoder({
            "processed": False,
            "status_code": e.status_code,
            "detail": e.detail
        })
    except Exception as e:
        return jsonable_encoder({
            "processed": False,
            "error": str(e)
        })