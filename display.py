import rich
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()


def print_welcome(features: list):
    """Prints the welcome message and available modes."""
    console.print("[bold cyan]Welcome! Select an initial mode:[/bold cyan]")
    for feature in features:
        console.print(
            f"  [bold yellow]{feature.number}[/bold yellow]: [green]{feature.description}[/green]"
        )
    console.print("Enter the number to set the mode, then enter your text.")
    console.print("You can switch modes anytime by entering the mode number.")
    console.print("Press Enter on an empty line to exit.")


def print_refined_output(title: str, content: str):
    """Prints the refined output in a formatted panel."""
    console.print(Panel(content, title=title, border_style="green"))


def print_error(message: str):
    """Prints an error message in a formatted panel."""
    console.print(Panel(message, title="Error", border_style="red"))


def get_user_input(prompt_text: str) -> str:
    """Gets user input with a formatted prompt."""
    return Prompt.ask(prompt_text)


def print_model_info(model_info: dict):
    """Prints model information in a table."""
    # Create a table instance
    table = Table(title="Model Configuration")

    # Add columns for Key and Value
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    # Populate the table with data from the dictionary
    for key, value in model_info.items():
        table.add_row(key, str(value))

    # Print the table to the console
    rich.print(table)
