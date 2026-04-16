import requests
from dotenv import load_dotenv
import os

load_dotenv()
AVWX_API_KEY = os.getenv("AVWX_API_KEY")

def getAirportInfoByIata(icao_code):
    headers = {'Authorization': AVWX_API_KEY}
    url = f"https://avwx.rest/api/station/{icao_code}"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
    except requests.Timeout as e:
        print(f"Request timed out while fetching airport information for {icao_code}: {e}")
        return None
    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        if status_code == 404:
            print(f"Airport information not found for {icao_code}.")
        elif status_code == 401:
            print("Unauthorized access. Check your API key.")
        elif status_code == 429:
            print("Rate limit exceeded. Please try again later.")
        else:
            print(f"HTTP error occurred for {icao_code}: {e}")
        return None
    except requests.RequestException as e:
        print(f"Network error while fetching airport information for {icao_code}: {e}")
        return None
    
    if not data.get('iata'):
        print(f"No airport information found for {icao_code}.")
    return data


def getMetarByIata(icao_code):
    headers = {'Authorization': AVWX_API_KEY}
    url = f"https://avwx.rest/api/metar/{icao_code}?airport=true"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
    except requests.Timeout as e:
        print(f"Request timed out while fetching METAR data for {icao_code}: {e}")
        return None
    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        if status_code == 404:
            print(f"METAR data not found for {icao_code}.")
        elif status_code == 401:
            print("Unauthorized access. Check your API key.")
        elif status_code == 429:
            print("Rate limit exceeded. Please try again later.")
        else:
            print(f"HTTP error occurred for {icao_code}: {e}")
        return None
    except requests.RequestException as e:
        print(f"Network error while fetching METAR data for {icao_code}: {e}")
        return None
    
    if not data.get('raw'):
        print(f"No METAR data found for {icao_code}.")
    return data