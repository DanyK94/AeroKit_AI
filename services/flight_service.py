#call the flight service to get the flight details
import os
import requests
from dotenv import load_dotenv
load_dotenv()

AIRLABS_API_KEY = os.getenv("AIRLABS_API_KEY")

keys = ["alt", "speed", "flight_iata", "dep_icao", "arr_icao", "aircraft_icao", "status"] # Define the keys you want to extract from the flight information

def getFlightDataByFNumber(fNum):
    url = f"https://airlabs.co/api/v9/flight?flight_iata={fNum}&api_key={AIRLABS_API_KEY}"

    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching flight data: {e}")
        return None   
    
    try:
        data = response.json() # Parse the JSON response
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    
    if not data.get('response'): # Check if the response contains flight information
        print("No flight information found for the given flight number.")
        return None
    
    return getDataByKey(data['response'], keys)  # Extract the specified keys from the flight information

def getDataByKey(flightInfo, keys):
    extracted_data = {}
    for key in keys:
        extracted_data[key] = flightInfo.get(key, "N/A")  # Use "N/A" if the key is not found
    return extracted_data