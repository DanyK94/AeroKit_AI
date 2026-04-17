import os
import requests
from dotenv import load_dotenv

load_dotenv()
AIRLABS_API_KEY = os.getenv("AIRLABS_API_KEY")

def getAirlineByIata(iata_code):
    url = f"https://airlabs.co/api/v9/airlines?iata_code={iata_code}&api_key={AIRLABS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['response']: # Check if the response contains data
        return data['response'][0]  # Return the first airline in the response
    return None  # Return None if no airline is found
