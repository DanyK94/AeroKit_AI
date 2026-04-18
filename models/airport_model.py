from dataclasses import dataclass
from models.runway_model import Runway

@dataclass
class Airport:
    icao: str
    name: str
    city: str
    country: str
    latitude: float
    longitude: float
    runways: list[Runway]

