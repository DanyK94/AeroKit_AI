from clients import airport_client
from models.weather_report import WeatherReport


def getMetarData(icao_code):
    rawMetar = airport_client.getMetarByIata(icao_code)
    airportInfo = airport_client.getAirportInfoByIata(icao_code)

    weatherReport = WeatherReport(
        airport=f"{icao_code} - {airportInfo.get('name', 'Unknown Name')}",
        observation=parseTime(rawMetar.get('time')),
        wind=parseWind([rawMetar.get('wind_direction'), rawMetar.get('wind_speed')]),
        visibility=parseVisibility(rawMetar.get('visibility')),
        clouds=parseClouds(rawMetar.get('clouds')),
        temperature=parseTemperature(rawMetar.get('temperature')),
        dew_point=parseDewPoint(rawMetar.get('dewpoint')),
        pressure=parseAltimeter(rawMetar.get('altimeter')),
        conditions=parseFlightRules(rawMetar.get('flight_rules'))
    )

    return weatherReport

def parseTime(timeData):
    # From 121250Z to 12th day, 12:51 UTC
    time = timeData.get('repr', '')  # Get the raw time string from the METAR data
    day = time[:2]
    time = time[2:6]
    return f"{day}th day, {time[:2]}:{time[2:]} UTC"

def parseWind(windData):
    return f"{windData[0].get('repr')}° at {windData[1].get('repr', 'Unknown')} knots"

def parseVisibility(visData):
    # From 1500 to 150 meter
    #if CAVOK then return "Ceiling And Visibility OK"
    visibility = visData.get('repr', '')  # Get the raw visibility string from the METAR data
    if visibility == "CAVOK":
        return "Ceiling And Visibility OK"
    elif visibility == "9999":
        return "10 kilometer or more"
    elif visibility == "0000":
        return "Less than 50 meters"
    return f"{visibility} meter"

def parseClouds(CloudData):

    rule = {
        "FEW": "Few clouds at {} feet",
        "SCT": "Scattered clouds at {} feet",
        "BKN": "Broken clouds at {} feet",
        "OVC": "Overcast clouds at {} feet",
        "SKC": "Sky Clear",
        "CLR": "Sky Clear"
    }
    if len(CloudData) == 0:
        return "Sky Clear"
    firstLayer = CloudData[0]
    altitude = firstLayer.get('altitude')
    altitude = int(altitude) * 100
    type = firstLayer.get('type')
    return rule.get(type).format(altitude)

def parseTemperature(tempData):
    return f"{tempData.get('repr', 'Unknown Temperature')}°C"

def parseDewPoint(dewData):
    return f"{dewData.get('repr', 'Unknown Dew Point')}°C"    

def parseAltimeter(altData):
    return f"{altData.get('value', 'Unknown Altimeter')} hPa"



def parseFlightRules(conditions):
    rules = {
        "VFR": "VFR (Visual Flight Rules)",
        "MVFR": "MVFR (Marginal Visual Flight Rules)",
        "IFR": "IFR (Instrument Flight Rules)",
        "LIFR": "LIFR (Low Instrument Flight Rules)"
    }
    return rules.get(conditions, "Unknown Conditions")