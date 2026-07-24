# ============================================================================
# USER MEMORY (Slide 14: "Preferences That Persist Across Sessions")
#
# What students will learn:
#   User memory is scoped to ONE user, persisted across every future
#   session. It solves "always format my reports as a table" without the
#   user repeating themselves every time.
#
# Why it matters:
#   Governance note (Slide 14): user memory is personal data - it needs the
#   same retention and deletion controls as any other PII store. We store
#   it in a plain JSON file here specifically so that governance point is
#   visible and inspectable, not hidden inside a database.
#
# Architecture:
#   data/user_memory.json  ->  { "<user_id>": { "<preference_key>": "<value>" } }
#
# Flow:
#   1. set_preference() writes a key/value under the user's id and saves to disk
#   2. get_preferences() reads the file fresh - simulating a brand-new
#      session that has never seen this user before, proving persistence
#
# Expected Output:
#   Demo 3 from the deck (Slide 17): a preference set in "session 1" is
#   read back correctly by a completely separate "session 2" read.
# ============================================================================

from pathlib import Path

from shared.console import console, section, step
from shared.mock_data import load_json, save_json


def set_preference(store_path: Path, user_id: str, key: str, value: str) -> None:
    """Trainer Note: this is the ONLY write path for user memory - it goes
    straight to disk so it survives past this Python process, unlike
    session_memory.py's in-RAM dict."""
    store = load_json(store_path)
    store.setdefault(user_id, {})
    store[user_id][key] = value
    save_json(store_path, store)


def get_preferences(store_path: Path, user_id: str) -> dict:
    """Trainer Note: reading here does NOT depend on any prior Python
    object still existing - a totally new process calling this function
    gets the same result. That's what makes it 'user memory' and not
    'session memory.'"""
    store = load_json(store_path)
    return store.get(user_id, {})


def demo_user_memory_persistence(store_path: Path, user_id: str) -> None:
    """Demo 3 from the deck (Slide 17): set a preference once, then prove a
    brand-new session already knows it without being told again."""
    section("Demo 3: Session + User Memory Build")

    step(1, "Set the preference in session 1")
    preference_text = "always format budget summaries as a table with variance highlighted in red"
    console.print(f'[bold green]User says:[/bold green] "From now on, {preference_text}."')
    set_preference(store_path, user_id, key="budget_summary_format", value=preference_text)

    step(2, "Start a fresh session 2 (a new, unrelated function call)")
    console.print("[dim]Simulating a brand-new session - no shared in-memory state with session 1.[/dim]")

    step(3, "Ask the same type of question in session 2")
    console.print('[bold green]User asks:[/bold green] "Give me this month\'s budget summary."')
    remembered = get_preferences(store_path, user_id)

    step(4, "Show the stored preference + how it was retrieved")
    if "budget_summary_format" in remembered:
        console.print(
            f"[bold magenta]Agent applies stored preference automatically:[/bold magenta] "
            f"{remembered['budget_summary_format']}"
        )
        console.print(
            "[bold cyan]No preference was restated - that's the entire "
            "user-memory pitch in one demo.[/bold cyan]"
        )
    else:
        console.print("[bold red]No stored preference found - something went wrong.[/bold red]")
