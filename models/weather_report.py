from dataclasses import dataclass


"""
Airport : KJFK - John F. Kennedy International 
Observation : 12th day, 12:51 UTC 
Wind : 240° at 8 knots 
Visibility : 10 statute miles 
Weather : Clear 
Clouds : Few clouds at 25,000 feet 
Temperature : -4°C 
Dew Point : -17°C 
Pressure : 30.34 inHg
Conditions : VFR (Visual Flight Rules)
"""
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