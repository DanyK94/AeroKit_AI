from rich.table import Table
from rich.panel import Panel
from rich.console import Console


def display_acronym_info(explanation):
    table = Table.grid(padding=(1, 1)) #
    table.add_column(style="bold cyan", width=10)  # Label column
    table.add_column()  # Value column

    table.add_row("Acronym", explanation.acronym)
    table.add_row("Definition", explanation.definition)
    table.add_row("Context", explanation.context)
    table.add_row("Example", explanation.example)
    table.add_row("Importance", explanation.importance)
    table.add_row("Related Acronyms", "\n".join(f"• {item}" for item in explanation.related)) # Add bullet points for related acronyms

    panel = Panel(
        table,
        title=f"ACRONYM EXPLANATION - {explanation.acronym.split(' - ')[0]}",
        border_style="cyan",
        padding=(1, 2)
    )
    console = Console()
    console.print(panel)