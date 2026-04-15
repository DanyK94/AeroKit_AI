from rich.table import Table
from rich.console import Console

console = Console()

table = Table(title="Flight Information")

table.add_column("Flight Number", style="cyan")
table.add_column("Departure", style="green")
table.add_column("Arrival", style="red")
table.add_column("Status", style="yellow")
table.add_column("Aircraft", style="white")
table.add_column("Altitude", style="magenta")
table.add_column("Speed", style="blue")

def add_flight_info_to_table(flight_info):
    table.add_row(
        flight_info.get("flight_iata", "N/A"),
        flight_info.get("dep_icao", "N/A"),
        flight_info.get("arr_icao", "N/A"),
        flight_info.get("status", "N/A"),
        flight_info.get("aircraft_icao", "N/A"),
        str(flight_info.get("alt", "N/A")),
        str(flight_info.get("speed", "N/A"))
    )
def display_table():
    console.print(table)