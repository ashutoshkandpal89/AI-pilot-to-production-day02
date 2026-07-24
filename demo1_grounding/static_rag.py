# ============================================================================
# STATIC RAG (the "Then" column from Slide 2 / Slide 6)
#
# What students will learn:
#   How a traditional RAG pipeline works - one embedding index, refreshed on
#   a schedule, retrieval happens ONCE before the model starts reasoning.
#
# Why it matters:
#   This is the baseline every other pattern in this repo improves on. If
#   students don't feel the limitation here, Foundry IQ's re-query behavior
#   in foundry_iq.py won't land.
#
# Architecture:
#   query -> single keyword search over a FIXED snapshot of documents
#         -> whatever comes back is ALL the agent ever sees for this answer
#
# Flow:
#   1. Build the index once (a snapshot, taken at "index time")
#   2. Search it once per question
#   3. No re-query, no permission filtering, no reasoning about what's missing
#
# Expected Output:
#   A single-pass answer built from whatever the one search call returned -
#   even if that's incomplete, and even if the source has since changed.
# ============================================================================

import copy

from shared.console import console, section, step


def build_static_index(documents: list[dict]) -> list[dict]:
    """Trainer Note: this is the 'nightly refresh' moment. deepcopy freezes
    a true snapshot - edits to the live documents after this line will NOT
    appear here until the index is rebuilt on its next scheduled refresh."""
    console.print(f"[dim]Static index built from {len(documents)} documents (snapshot, not live).[/dim]")
    return copy.deepcopy(documents)


def static_rag_search(index: list[dict], query: str) -> list[dict]:
    """Trainer Note: one keyword match, one shot. No iteration, no
    re-ranking mid-task - this is the 'lookup' Foundry IQ is contrasted
    against on Slide 6."""
    query_terms = query.lower().split()
    matches = []
    for doc in index:
        haystack = (doc["title"] + " " + doc["content"]).lower()
        if any(term in haystack for term in query_terms):
            matches.append(doc)
    return matches


def demo_static_rag_limitation(documents: list[dict]) -> None:
    """Trainer Note: run this before foundry_iq's demo to set up the
    contrast live. Shows a static index missing a multi-part question and
    never noticing a source document changed."""
    section("Static RAG (the baseline we're improving on)")

    index = build_static_index(documents)

    step(1, "Ask a multi-part question in one shot")
    query = "Q3 expansion timeline and headcount budget"
    console.print(f'[bold green]Question:[/bold green] "{query}"')

    results = static_rag_search(index, query)
    console.print(f"[bold]Single search returned {len(results)} document(s):[/bold]")
    for doc in results:
        console.print(f"  - {doc['title']}")

    step(2, "Update the LIVE source document AFTER the index was built")
    live_doc = documents[0]
    live_doc["content"] += " [UPDATED: DACH entry pushed to month 2.]"
    console.print(f"[yellow]Edited '{live_doc['title']}' in the live source...[/yellow]")

    step(3, "Re-ask the identical question - but the index is still frozen")
    stale_results = static_rag_search(index, query)
    console.print(
        "[bold red]Static RAG has no re-query step - it searches the SAME frozen "
        "index built in Step 1, so the edit above is invisible until the next "
        "scheduled refresh.[/bold red]"
    )
    console.print(f"[dim]({len(stale_results)} documents matched - identical to Step 1, by design.)[/dim]")
