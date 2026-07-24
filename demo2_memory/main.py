# ============================================================================
# DEMO 2: ENTERPRISE MEMORY - Session, User, and Procedural Memory
#
# What students will learn:
#   The three-memory ladder (Slide 12): scope increases left to right, from
#   one conversation, to one user across time, to every user of a workflow.
#
# Why it matters:
#   Matching the memory type to the job is the field-notes takeaway from
#   Slide 16 - most teams default correctly to session memory, then miss
#   procedural memory, which has the highest ROI.
#
# Architecture:
#   session_memory.py     -> in-RAM only, one conversation
#   user_memory.py        -> data/user_memory.json, one user, many sessions
#   procedural_memory.py  -> data/procedural_memory.json, shared across users
#
# Flow: run this file directly. It resets both JSON stores to a clean
# state, then walks session scope, user memory persistence (Demo 3), and
# procedural memory (Demo 4), in the order narrated in the deck.
#
# Expected Output:
#   Three sections: a session-scope proof, a cross-session preference
#   recall, and a taught reconciliation procedure applied to a new batch.
# ============================================================================

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.console import console, section
from shared.config import print_mode_banner
from shared.mock_data import load_json, save_json, TEST_USER_A_FINANCE
from session_memory import demo_session_scope
from user_memory import demo_user_memory_persistence
from procedural_memory import demo_procedural_memory

USER_MEMORY_PATH = Path(__file__).parent / "data" / "user_memory.json"
PROCEDURAL_MEMORY_PATH = Path(__file__).parent / "data" / "procedural_memory.json"
INVOICE_BATCH_PATH = Path(__file__).parent / "data" / "invoice_batch.json"


def _reset_stores() -> None:
    """Trainer Note: run before every demo so the JSON files start empty,
    exactly like a fresh Foundry project - re-run this file as many times
    as you like during rehearsal."""
    save_json(USER_MEMORY_PATH, {})
    save_json(PROCEDURAL_MEMORY_PATH, {})


def main() -> None:
    console.rule("[bold]DEMO 2: ENTERPRISE MEMORY - Session, User, Procedural[/bold]")
    print_mode_banner()
    _reset_stores()

    section("Memory Scope Ladder: Session Memory")
    demo_session_scope()

    demo_user_memory_persistence(USER_MEMORY_PATH, TEST_USER_A_FINANCE.user_id)

    invoices = load_json(INVOICE_BATCH_PATH)
    demo_procedural_memory(PROCEDURAL_MEMORY_PATH, invoices)

    section("Demo 2 complete")
    console.print(
        "[bold green]Recap:[/bold green] Session = free, table stakes. "
        "User = preferences, needs PII-level governance. "
        "Procedural = highest ROI, taught once, reused by everyone."
    )


if __name__ == "__main__":
    main()
