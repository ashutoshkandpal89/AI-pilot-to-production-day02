# Trainer Note:
# Every demo prints through these helpers instead of calling print() or
# Console() directly, so the whole repo has one consistent "look" on
# screen - useful when you're narrating four demos back-to-back live.
#
# Rich is a formatting library only. It draws boxes and colors around text
# you already have - it doesn't call any AI model or service itself.

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

console = Console()


def section(title: str) -> None:
    """A big divider - use this when moving into a new demo or stage."""
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/bold cyan]"))


def step(number: int, label: str) -> None:
    """A numbered step inside a demo - mirrors the 'presenter flow' steps
    printed on each demo slide in the deck."""
    console.print(f"[bold yellow]Step {number}:[/bold yellow] {label}")


def trainer_note(text: str) -> None:
    """Prints a note in a muted style - use for asides you'd say out loud
    but that aren't part of the 'official' agent output."""
    console.print(f"[dim italic]Trainer note: {text}[/dim italic]")


def user_prompt(user_label: str, prompt_text: str) -> None:
    console.print(Panel(prompt_text, title=f"[bold green]{user_label} asks[/bold green]", expand=False))


def agent_answer(answer_text: str) -> None:
    console.print(Panel(answer_text, title="[bold magenta]Agent answer[/bold magenta]", expand=False))


def denied(reason: str) -> None:
    console.print(Panel(reason, title="[bold red]Access denied / restricted[/bold red]", expand=False))


def retrieval_trace_table(trace) -> None:
    """Renders a RetrievalTrace (shared.models.RetrievalTrace) as a table.
    This is the 'show retrieval trace' moment from Demo 1's slide."""
    table = Table(title="Retrieval Trace (Foundry IQ simulation)")
    table.add_column("Step", style="bold")
    table.add_column("Query Issued")
    table.add_column("Docs Found")
    table.add_column("Reasoning")
    for s in trace.steps:
        table.add_row(str(s.step_number), s.query_issued, ", ".join(s.docs_found) or "-", s.reasoning)
    console.print(table)
    if trace.docs_filtered_by_permission:
        console.print(
            f"[bold red]Filtered by permission (not shown to this user):[/bold red] "
            f"{', '.join(trace.docs_filtered_by_permission)}"
        )


def key_value_panel(title: str, data: dict) -> None:
    table = Table(show_header=False, box=None)
    table.add_column("Key", style="bold")
    table.add_column("Value")
    for k, v in data.items():
        table.add_row(str(k), str(v))
    console.print(Panel(table, title=title, expand=False))
