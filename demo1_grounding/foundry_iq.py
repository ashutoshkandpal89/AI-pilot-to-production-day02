# ============================================================================
# FOUNDRY IQ SIMULATION (the "Now" column from Slide 2 / Slide 6)
#
# What students will learn:
#   Retrieval as a reasoning step - the agent decides WHAT to look up,
#   issues more than one query inside a single answer, and re-queries a
#   live source instead of a frozen snapshot.
#
# Why it matters:
#   This is Demo 1 from the deck (Slide 9): "Show retrieval happening as
#   an iterative reasoning step, not a one-shot lookup."
#
# Architecture (Slide 8, narrated left to right):
#   User Query -> Reasoning-Driven Retrieval -> Permission Filter -> Grounded Answer
#
# Flow:
#   1. Split the question into sub-questions (the "reasoning" step)
#   2. Issue one retrieval query per sub-question, recording each step
#   3. Re-run the LIVE search (not a frozen index) so edits are always seen
#   4. Hand the results to permission_filter.py before answering
#
# Expected Output:
#   A RetrievalTrace with 2+ steps, and an answer that reflects a live
#   source edit immediately - no waiting for a scheduled re-index.
# ============================================================================

from shared.console import console, section, step, retrieval_trace_table
from shared.models import RetrievalTrace


STOPWORDS = {"q3", "expansion", "plan", "our", "the", "and", "a", "of"}


def _live_search(documents: list[dict], query: str) -> list[dict]:
    """Trainer Note: unlike static_rag_search, this always runs against the
    CURRENT documents list - there is no frozen snapshot to go stale.
    Stopwords are dropped and ALL remaining terms must match, so each
    sub-question in the trace retrieves a distinct, meaningful subset."""
    query_terms = [t for t in query.lower().split() if t not in STOPWORDS]
    matches = []
    for doc in documents:
        haystack = (doc["title"] + " " + doc["content"]).lower()
        if query_terms and all(term in haystack for term in query_terms):
            matches.append(doc)
    return matches


def _split_into_subquestions(question: str) -> list[str]:
    """Trainer Note: a real Foundry IQ agent decides this dynamically with
    the model itself. We hard-code the decomposition here so the AUDIENCE
    can see the exact reasoning steps without an actual model call."""
    return [
        "Q3 expansion timeline milestones",
        "Q3 expansion headcount budget",
    ]


def foundry_iq_answer(documents: list[dict], question: str) -> tuple[str, RetrievalTrace]:
    """Runs the multi-step retrieval loop and returns (answer_text, trace)."""
    trace = RetrievalTrace()
    all_found: list[dict] = []

    for sub_q in _split_into_subquestions(question):
        found = _live_search(documents, sub_q)
        trace.add_step(
            query=sub_q,
            docs_found=[d["doc_id"] for d in found],
            reasoning=f"Sub-question needed to fully answer: '{question}'",
        )
        for doc in found:
            if doc not in all_found:
                all_found.append(doc)

    answer_lines = [f"- {d['title']}: {d['content']}" for d in all_found]
    answer = "\n".join(answer_lines) if answer_lines else "No matching documents found."
    return answer, trace


def demo_dynamic_retrieval(documents: list[dict]) -> None:
    """Demo 1 from the deck (Slide 9): multi-part question, show the trace,
    point out the re-query step, update a source doc, and re-ask."""
    section("Demo 1: Foundry IQ Dynamic Retrieval Walkthrough")

    question = "Answer this multi-part question about our Q3 expansion plan: timeline and headcount budget."

    step(1, "Ask the multi-part question")
    console.print(f'[bold green]Question:[/bold green] "{question}"')
    answer, trace = foundry_iq_answer(documents, question)

    step(2, "Show the retrieval trace mid-answer")
    retrieval_trace_table(trace)
    console.print(f"[bold]Answer:[/bold]\n{answer}")

    step(3, "Point out the re-query step")
    console.print(
        f"[cyan]Notice trace step count = {len(trace.steps)} - Foundry IQ issued "
        "more than one query for a single answer. Static RAG issues exactly one, "
        "always.[/cyan]"
    )

    step(4, "Update a source doc and re-ask")
    documents[0]["content"] += " [UPDATED: DACH entry pushed to month 2 due to reseller delay.]"
    documents[0]["version"] += 1
    console.print(f"[yellow]Edited '{documents[0]['title']}' (now version {documents[0]['version']})...[/yellow]")

    updated_answer, updated_trace = foundry_iq_answer(documents, question)
    console.print(f"[bold]Re-asked answer (reflects the edit immediately):[/bold]\n{updated_answer}")
    retrieval_trace_table(updated_trace)
