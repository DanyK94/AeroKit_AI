import os
import sys
from clients.airline_client import *
from clients.flight_client import *
from tables.flight_table import *
from tables.functions_table import *
from tables.metar_table import *
from services.metar_service import *

def main():
    print("Welcome to AeroKit AI!")
    chooseFunctionality()

def chooseFunctionality():
    functions = [
        {"name": "Get Flight Information", "description": "Retrieves real-time flight information based on flight number or route"},
        {"name": "Get Airline Information", "description": "Retrieves information about a specific airline based on its IATA or ICAO code"},
        {"name": "Get METAR Weather Report", "description": "Retrieves the latest METAR weather report for a specific airport"},
        {"name": "Exit", "description": "Exits the AeroKit AI application"}
    ]
    while True:
        display_functions_table(functions)
        choice = input("Enter the number of the function you want to use: ")
        if choice == "1":
            flightInformation()
        elif choice == "2":
            airlineInformation()
        elif choice == "3":
            metarInformation()
        elif choice == "4":
            print("Exiting AeroKit AI. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a function listed in the table.")
        input("\nPress Enter to continue...") # Wait for user input before showing the functions table again

def flightInformation():
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
    
def airlineInformation():
    iata_code = input("Enter the IATA code of the airline: ").strip().upper() # Get the IATA code input from the user and convert to uppercase
    airline_info = getAirlineByIcao(iata_code) #To Improve: Validation Input
    if airline_info:
        print(f"Airline Name: {airline_info.get('name', 'N/A')}")
        print(f"Airline IATA Code: {airline_info.get('iata_code', 'N/A')}")
        print(f"Airline ICAO Code: {airline_info.get('icao_code', 'N/A')}")
    else:
        print("No airline information found for the given ICAO code.")
    return

def metarInformation():
    icao_code = input("Enter the ICAO code of the airport: ").strip().upper() # Get the ICAO code input from the user and convert to uppercase
    metar_info = getMetarData(icao_code) # Call the METAR service to get the weather report for the specified airport
    if metar_info:
        #display_metar_info(metar_info) # Display the METAR information in a table format [OLD]
        display_metar_panel(metar_info) # Display the METAR information in a panel format
    else:
        print("No METAR information found for the given ICAO code.")
    return

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