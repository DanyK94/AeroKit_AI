from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class WeatherReport:
    airport: str
    observation: str
    wind: str
    visibility: str
    clouds: str
    temperature: str
    dew_point: str
    pressure: str
    conditions: str

class Wind(BaseModel):
    direction: int
    speed_kt: int

class Metar(BaseModel):
    raw: str
    temperature_c: int
    dewpoint_c: int
    wind: Wind
    visibility_sm: int
    condition: str

class AirportMetarResponse(BaseModel):
    airport: str
    metar: Metar
    timestamp: str