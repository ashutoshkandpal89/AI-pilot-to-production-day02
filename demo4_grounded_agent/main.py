# ============================================================================
# DEMO 4: COMPLETE ENTERPRISE GROUNDED AGENT (the climax)
#
# What students will learn:
#   Grounding + Permission + Memory + Procedure + Tool Discovery + Enterprise
#   Connector, all combined into one live answer to one real question.
#
# Why it matters:
#   Demo 7 (Slide 28): "Assemble everything from today into one agent,
#   live... answering a real business question correctly and safely."
#
# Architecture:
#   grounded_agent.py's run_grounded_query() wires together demo1, demo2,
#   and demo3's modules - nothing is reimplemented here.
#
# Flow: run this file directly. It states the design checklist out loud,
# runs the full grounded query as Test User A (Finance), shows every
# stage, then re-runs as Test User B (Sales) and compares.
#
# Expected Output:
#   Test User A gets a full reconciliation verdict with sources,
#   procedure, and tool trace. Test User B is stopped at the permission
#   gate before any financial data is touched.
# ============================================================================

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.console import console, section, step, user_prompt, agent_answer, denied, key_value_panel
from shared.config import print_mode_banner
from shared.mock_data import TEST_USER_A_FINANCE, TEST_USER_B_SALES
from grounded_agent import run_grounded_query

QUESTION = (
    "Using our reconciliation procedure, our SharePoint finance library, and the "
    "expense-lookup tool, tell me if this vendor invoice batch is ready to approve."
)


def _print_checklist() -> None:
    """The grounded-agent design checklist from Slide 27, said out loud
    before the query runs - not just decoration, an actual pre-flight
    check a trainer narrates live."""
    step(1, "State the design checklist out loud first")
    key_value_panel(
        "Grounded-Agent Design Checklist",
        {
            "1. Retrieval": "Is grounding one-shot, or does this need iterative retrieval?",
            "2. Permissions": "Does every data path resolve against the calling user?",
            "3. Memory & Tools": "What persists (procedure), what's discovered (tool)?",
        },
    )


def _print_result(user_label: str, result) -> None:
    if not result.permitted:
        denied(result.verdict)
        return

    agent_answer(result.verdict)

    console.print("[bold]Sources used:[/bold]")
    for s in result.sources_used:
        console.print(f"  - {s}")

    console.print(f"[bold]Procedure used:[/bold] {result.procedure_used}")

    console.print("[bold]Reconciliation results:[/bold]")
    for r in result.reconciliation_results:
        flag = "[bold red]FLAGGED[/bold red]" if r["flagged"] else "[green]OK[/green]"
        approved = "approved" if r["budget_approved"] else "[bold red]NOT approved[/bold red]"
        console.print(f"  {r['invoice_id']} (PO {r['po_number']}): {flag}, budget {approved}")

    if result.tool_trace:
        console.print(f"[bold]Tool trace (expense-lookup):[/bold]\n{result.tool_trace}")


def main() -> None:
    console.rule("[bold]DEMO 4: COMPLETE ENTERPRISE GROUNDED AGENT[/bold]")
    print_mode_banner()
    section("Demo 7: Climax - Building a Grounded Agent End-to-End")

    _print_checklist()

    step(2, "Run the full grounded query as Test User A (Finance)")
    user_prompt(TEST_USER_A_FINANCE.display_name, QUESTION)
    result_a = run_grounded_query(TEST_USER_A_FINANCE)

    step(3, "Show sources + permission trace + procedure used")
    _print_result(TEST_USER_A_FINANCE.display_name, result_a)

    step(4, "Re-run as a lower-permission user, compare")
    user_prompt(TEST_USER_B_SALES.display_name, QUESTION)
    result_b = run_grounded_query(TEST_USER_B_SALES)
    _print_result(TEST_USER_B_SALES.display_name, result_b)

    section("Demo 4 complete")
    console.print(
        "[bold cyan]Every pattern from today just showed up in one live answer: "
        "reasoning-driven retrieval, permission enforcement, procedural memory, "
        "and a discovered tool. That's the whole session in one demo.[/bold cyan]"
    )


if __name__ == "__main__":
    main()
