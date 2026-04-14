import os
import requests
from dotenv import load_dotenv

load_dotenv()
AIRLABS_API_KEY = os.getenv("AIRLABS_API_KEY")

def getAirlineByIcao(icao_code):
    url = f"https://airlabs.co/api/v9/airlines?icao_code={icao_code}&api_key={AIRLABS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['response']: # Check if the response contains data
        return data['response'][0]  # Return the first airline in the response
    return None  # Return None if no airline is found

def printAirlineInfo(airline_info):
    print ("\n --- Airline Information ---")
    for key, value in airline_info.items():
        print(f"{key.upper():20}: {value}")