from rich.table import Table
from rich.console import Console


def create_functions_table():
    table = Table(title="Available Functions") # Create a table with the title "Available Functions"
    
    # Define the columns for the functions table with appropriate styles
    table.add_column("No.", style="bold cyan", width=5) # Column for the function number (e.g., "1", "2")
    table.add_column("Function Name", style="cyan", width=30) # Column for the function name (e.g., "Get Flight Information")
    table.add_column("Description", style="white", width=50) # Column for the function description (e.g., "Retrieves real-time flight information based on flight number or route")
    return table

def display_functions_table(functions):
    table = create_functions_table()  # Create a new table instance
    i = 1

    for func in functions:
        table.add_row(str(i), func['name'], func['description']) # Add a row to the table for each function with its number, name, and description
        i += 1
    console = Console()
    console.print(table)