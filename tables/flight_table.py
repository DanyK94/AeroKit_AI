from rich.table import Table
from rich.console import Console
from config import DEFAULT_VALUE

console = Console()


def create_flight_table():

    table = Table(title="Flight Information") # Create a table with the title "Flight Information"
    
    # Define the columns for the flight information table with appropriate styles
    table.add_column("No.", style="bold cyan", width=5)
    table.add_column("Flight Number", style="cyan", width=15)
    table.add_column("Departure", style="green", width=12)
    table.add_column("Arrival", style="red", width=12)
    table.add_column("Status", style="yellow", width=15)
    table.add_column("Aircraft", style="white", width=12)
    table.add_column("Altitude", style="magenta", width=12)
    table.add_column("Speed", style="blue", width=10)
    return table

def display_flight_info(flights_info):
    table = create_flight_table()  # Create a new table instance
    i = 1

    for flight_info in flights_info:

        status = flight_info.get("status", DEFAULT_VALUE)

        table.add_row(
            str(i),          
            str(flight_info.get("flight_iata", DEFAULT_VALUE)),
            str(flight_info.get("dep_icao", DEFAULT_VALUE)),
            str(flight_info.get("arr_icao", DEFAULT_VALUE)),
            f"{get_status_icon(status)} {status}",
            str(flight_info.get("aircraft_icao", DEFAULT_VALUE)),
            str(flight_info.get("alt", DEFAULT_VALUE)),
            str(flight_info.get("speed", DEFAULT_VALUE))
        )
        i += 1
    console.print(table)


def get_status_icon(status):
    status_icons = {
        "scheduled": "🗓️ ",
        "en-route": "✈️ ",
        "landed": "🛬 ",
        "cancelled": "❌ ",
        "diverted": "🔀 ",
        "incident": "⚠️ ",
        "unknown": "❓ "
    }
    return status_icons.get(status.lower(), "❓ ")