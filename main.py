import os
from services.airline_service import *

def main():
    print("Welcome to AeroKit AI!")
    icao = input("Enter an ICAO code to get airline information: ")
    if len(icao) > 3:
        print("Invalid ICAO code. Please enter a 3-letter code.")
        return
    airline_info = getAirlineByIcao(icao)
    printAirlineInfo(airline_info)

if __name__ == "__main__":
    main()