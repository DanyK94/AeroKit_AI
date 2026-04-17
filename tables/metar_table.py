from rich.table import Table
from rich.console import Console
from rich.panel import Panel

def display_metar_panel(metar_info):
    ## Create a grid table for displaying METAR information in a panel format
    table = Table.grid(padding=(0, 1)) #
    table.add_column(style="bold cyan", width=15)  # Label column
    table.add_column()  # Value column

    ## Add rows to the table for each METAR parameter and its corresponding value, with an empty row for spacing before the flight conditions
    table.add_row("Airport", metar_info.airport)
    table.add_row("Observation", metar_info.observation)
    table.add_row("Wind", metar_info.wind)
    table.add_row("Visibility", metar_info.visibility)
    table.add_row("Clouds", metar_info.clouds)
    table.add_row("Temperature", metar_info.temperature)
    table.add_row("Dew Point", metar_info.dew_point)
    table.add_row("Pressure", metar_info.pressure)
    table.add_row("", "")  # Empty row for spacing
    table.add_row("Flight Conditions", f"[bold]{metar_info.conditions}[/bold]")

    ## Create a panel to display the METAR information with a title and border styling
    panel = Panel(
        table,
        title=f"METAR WEATHER REPORT - {metar_info.airport.split(' - ')[0]}",
        border_style="cyan",
        padding=(1, 2)
    )

    ## Display the panel using the Rich console
    console = Console()
    console.print(panel)