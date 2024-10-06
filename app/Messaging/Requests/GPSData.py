from pydantic import BaseModel

class GPSData(BaseModel):
    latitude: float
    longitude: float