from clients.airport_client import *
from models.airport_model import Airport
from models.runway_model import Runway
from models.weather_report import *
from clients.openai_client import getResponseFromAI
import re


def getAirportInformation(icao_code):
    data = getAirportInfoByIcao(icao_code)
    if data.get('error') is not None:
        return None
    return parseAirportInfo(data)

def getWeatherReport(icao_code):
    metar = getMetarByIcao(icao_code)
    weatherReport = parseMetarWeather(metar)
    return weatherReport

def getListAirportByKeyword(keyword):
    prompt = f"""Give me a list of 3 airport's icao code related to the keyword:{keyword} sorted by importance and relevance to the keyword:
    Format the response EXACTLY as the example that follow:
    LIRU, LIRF, LIRA
    DON'T Write explanation neither the prompt. the output MUST BE only a list as FOLLOW: LIRU, LIRF, LIRA
    """
    airports : list[Airport] = []

    response = getResponseFromAI(prompt)
    if response:
        #icao_list = response.split(', ') OLD
        icao_list = re.findall(r'\b[A-Z]{4}\b') #REGEX FIND 4-LETTER CODES
    else:
        return None
    for port in icao_list:
        airports.append(getAirportInformation(port))
    return airports

    


def parseMetarWeather(data):

    wind = Wind(
        direction = data.get('wind_direction',{}).get('value',0),
        speed_kt = data.get('wind_speed',{}).get('value')
    )

    metar = Metar(
        raw = data.get('raw'),
        temperature_c = data.get('temperature',{}).get('value'),
        dewpoint_c = data.get('dewpoint',{}).get('value'),
        wind = wind,   
        visibility_sm = data.get("visibility", {}).get("value", 0),
        condition = data.get('flight_rules')      
    )

    airportWeather = AirportMetarResponse(
        airport = data.get('station'),
        metar = metar,
        timestamp = data.get('time',{}).get('dt')
         
    )
    return airportWeather

def parseAirportInfo(data):

    rawRunways = data.get('runways')
    runways : list[Runway] = []
    for r in rawRunways:
        runways.append(parseRunway(r))

    airport_data = Airport(
        icao= data.get('icao'),
        name= data.get('name'),
        city= data.get('city'),
        country= data.get('country'),
        latitude = data.get('latitude'),
        longitude= data.get('longitude'),
        runways=runways
    )
    
    
    return airport_data

def parseRunway(rw):
    runways = Runway(
        bearing_1 = rw.get('bearing1'), 
        bearing_2 = rw.get('bearing2'), 
        ident_1 = rw.get('ident1'), 
        ident_2 = rw.get('ident2'), 
        length_ft = rw.get('length_ft'), 
        lights = rw.get('lights'), 
        surface = rw.get('surface')
    )
    return runways
