import os
import sys
from services.airline_service import *
from services.flight_service import *
from tables.flightTable import *

def main():
    print("Welcome to AeroKit AI!")
    fNum = input("Enter a flight number to get flight information: ")

    if not checkInput(fNum):
        return

    print(f"Fetching information for flight: {fNum}...")   

    flight_info = getFlightDataByFNumber(fNum)

    if flight_info is None:
        print("No flight information found for the given flight number.")
        return
    
    try:
        add_flight_info_to_table(flight_info)
        display_table()
    except Exception as e:
        print(f"An error occurred while displaying flight information: {e}")
        sys.exit(1)
    

def checkInput(fNum):
    if not fNum:
        print("Flight number cannot be empty")
        return False
    elif len(fNum) < 6:
        print("Invalid flight number. Please enter a 6-character code.")
        return False
    return True


def printAll(datas):
    for key, value in datas.items():
        print (f"{key.upper()}: {value}")








if __name__ == "__main__":
    main()