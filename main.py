import os
import sys
from services.airline_service import *
from services.flight_service import *
from tables.flightTable import *

def main():
    print("Welcome to AeroKit AI!")
    print("Enter flights numbers separated by comma to get flights information: ")
    fNums = input("Flight Numbers: ").split(",") # Get flight numbers input from the user and split by comma

    for fnum in fNums:
        fNum = fnum.strip() # Remove any leading/trailing whitespace from the flight number
        if not checkInput(fNum): 
            print(f"Skipping invalid flight number: {fNum}")
            fNums.remove(fnum) # Remove the invalid flight number from the list
            continue

    if len(fNums) > 0:
        flights = getFlightDataByFNumber(fNums) # Call the flight service to get the flight details
    else:
        print("No valid flight numbers entered. Exiting AeroKit AI.")
        sys.exit(1)

    
    try:
        display_flight_info(flights)
    except Exception as e:
        print(f"An error occurred while displaying flight information: {e}")
        sys.exit(1)
    
    # Ask the user if they want to get airline information
    choice = input("Do you want to get Airline information? (y/n): ")
    if choice.lower() == 'y':
        numRow = input("Enter the row number of the flight to get airline information: ")
        fNum = flights[int(numRow) - 1].get("flight_iata", "N/A")
        iata_code = fNum[:2].upper() # Extract the airline IATA code from the flight number (first two characters)
        if iata_code == "N/A":
            print("No aircraft IATA code found in flight information.")
            return
        
        airline_info = getAirlineByIcao(iata_code)
        if airline_info:
            print(f"Airline Name: {airline_info.get('name', 'N/A')}")
            print(f"Airline IATA Code: {airline_info.get('iata_code', 'N/A')}")
            print(f"Airline ICAO Code: {airline_info.get('icao_code', 'N/A')}")
        else:
            print("No airline information found for the given ICAO code.")
    else:
        print("Exiting AeroKit AI. Goodbye!")

def checkInput(fNum):
    if not fNum:
        print("Flight number cannot be empty")
        return False
    elif len(fNum) < 2:
        print("Invalid Flight number. Must be at least 2 character code")
        return False
    return True

if __name__ == "__main__":
    main()