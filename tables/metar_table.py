from rich.table import Table
from rich.console import Console


def create_metar_table(icao_code):

    table = Table(title=f"METAR WEATHER REPORT - {icao_code}") # Create a table with the title "METAR Information"
    
    # Define the columns for the METAR information table with appropriate styles
    table.add_column(style="bold cyan", width=20) # Column for the parameter name (e.g., "Temperature", "Wind Speed")
    table.add_column(style="white", width=40) # Column for the parameter value (e.g., "15°C", "10 knots")
    return table


def display_metar_info(metar_info):
    table = create_metar_table(metar_info.airport.split(" - ")[0])  # Create a new table instance with the airport code as the title

    # Add rows to the table for each METAR parameter and its corresponding value
    table.add_row("Airport", metar_info.airport)
    table.add_row("Observation", metar_info.observation)
    table.add_row("Wind", metar_info.wind)
    table.add_row("Visibility", metar_info.visibility)
    table.add_row("Clouds", metar_info.clouds)
    table.add_row("Temperature", metar_info.temperature)
    table.add_row("Dew Point", metar_info.dew_point)
    table.add_row("Pressure", metar_info.pressure)
    table.add_row("Flight Conditions", metar_info.conditions)

    console = Console()
    console.print(table)