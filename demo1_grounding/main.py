# ============================================================================
# DEMO 1: GROUNDING - Foundry IQ + Permission-Aware Retrieval
#
# What students will learn:
#   - The difference between static RAG and Foundry IQ's retrieval-as-
#     reasoning (Slide 6)
#   - Why permission-aware grounding is non-negotiable (Slide 7)
#   - How a query actually resolves, left to right (Slide 8)
#
# Why it matters:
#   Most "enterprise AI pilot" failures happen here - not on model quality,
#   but on stale retrieval and permission leaks (Slide 2).
#
# Architecture:
#   documents.json --> static_rag.py   (baseline, one-shot, frozen index)
#                   --> foundry_iq.py  (iterative, live, re-query capable)
#                   --> permission_filter.py (per-user visibility)
#
# Flow: run this file directly. It walks all three parts in order, exactly
# as narrated in the deck (Slides 9 then 10).
#
# Expected Output:
#   Three sections printed to the console: the static RAG limitation, the
#   Foundry IQ dynamic retrieval trace, and the two-user permission
#   comparison.
# ============================================================================

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.console import console, section
from shared.config import print_mode_banner
from shared.mock_data import load_json, TEST_USER_A_FINANCE, TEST_USER_B_SALES
from static_rag import demo_static_rag_limitation
from foundry_iq import demo_dynamic_retrieval
from permission_filter import demo_permission_aware_grounding

DATA_PATH = Path(__file__).parent / "data" / "documents.json"


def main() -> None:
    console.rule("[bold]DEMO 1: GROUNDING - Foundry IQ + Permission-Aware Retrieval[/bold]")
    print_mode_banner()

    # Trainer Note: load a FRESH copy of the documents for each part below,
    # so edits made in one part (e.g. the source-doc update in Foundry IQ)
    # don't bleed into the next part's starting state.
    demo_static_rag_limitation(load_json(DATA_PATH))
    demo_dynamic_retrieval(load_json(DATA_PATH))
    demo_permission_aware_grounding(load_json(DATA_PATH), TEST_USER_A_FINANCE, TEST_USER_B_SALES)

    section("Demo 1 complete")
    console.print(
        "[bold green]Recap:[/bold green] Static RAG = one-shot, frozen. "
        "Foundry IQ = iterative, live. Permission filter = always applied "
        "before the answer step, never after."
    )


if __name__ == "__main__":
    main()
