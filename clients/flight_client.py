#call the flight service to get the flight details
import os
import requests
from dotenv import load_dotenv
from core.config import DEFAULT_VALUE

load_dotenv()

AIRLABS_API_KEY = os.getenv("AIRLABS_API_KEY")

keys = ["alt", "speed", "flight_iata", "dep_icao", "arr_icao", "aircraft_icao", "status"] # Define the keys you want to extract from the flight information

def getFlightDataByFNumber(fNums):
    flights = []

    for fNum in fNums:
        url = f"https://airlabs.co/api/v9/flight?flight_iata={fNum}&api_key={AIRLABS_API_KEY}"

        try:
            response = requests.get(url, timeout=10)  # Set a timeout for the request
            response.raise_for_status()  # Raise an exception for HTTP errors

        except requests.Timeout:
            print(f"Request timed out while fetching flight data for {fNum}.")
            continue
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            if status_code == 404:
                print(f"Flight not found for {fNum}.")
            elif status_code == 401:
                print("Unauthorized access. Check your API key.")
            elif status_code == 429:
                print("Rate limit exceeded. Please try again later.")
            else:
                print(f"HTTP error occurred for {fNum}: {e}")
            continue
        except requests.RequestException as e:
            print(f"Network error while fetching {fNum}: {e}")
            continue

        try:
            data = response.json()  # Parse the JSON response
        except ValueError as e:
            print(f"Error parsing JSON response for {fNum}: {e}")
            continue

        if not data.get('response'):  # Check if the response contains flight information
            print(f"No flight information found for {fNum}.")
            continue

        flights.append(getDataByKey(data['response'], keys))  # Extract the relevant flight information using the defined keys and add it to the flights list
    return flights

def getDataByKey(flightInfo, keys):
    extracted_data = {}
    for key in keys:
        extracted_data[key] = flightInfo.get(key, DEFAULT_VALUE)  # Use DEFAULT_VALUE if the key is not found
    return extracted_data