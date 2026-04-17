from dataclasses import dataclass

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