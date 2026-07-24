# ============================================================================
# PROCEDURAL MEMORY (Slide 15: "The One Most Teams Miss")
#
# What students will learn:
#   Procedural memory is scoped to a TASK PATTERN, shared across every user
#   who performs it. It solves an agent re-deriving the correct multi-step
#   procedure from scratch every single run.
#
# Why it matters:
#   The highest-ROI memory type for recurring enterprise workflows, and the
#   one most pilots never implement (Slide 15). This is Demo 4 from the
#   deck (Slide 18) - teach the reconciliation procedure once, then apply
#   it to a batch the agent has never seen.
#
# Architecture:
#   data/procedural_memory.json -> { "<procedure_name>": {steps, match_field,
#                                     variance_threshold_pct, escalate_to} }
#
# Flow:
#   1. teach_procedure() stores the structured procedure once
#   2. run_reconciliation() loads the STORED procedure (never re-taught)
#      and applies it to a brand-new invoice batch
#
# Expected Output:
#   All three steps (match, flag, escalate) run correctly on a new batch
#   without the procedure being restated anywhere in this file's demo code.
# ============================================================================

from pathlib import Path

from shared.console import console, section, step, key_value_panel
from shared.mock_data import load_json, save_json


def teach_procedure(
    store_path: Path,
    name: str,
    steps: list[str],
    match_field: str,
    variance_threshold_pct: float,
    escalate_to: str,
) -> None:
    """Trainer Note: this is said ONCE, out loud, in the narration - after
    this call, run_reconciliation() below never needs the steps repeated."""
    store = load_json(store_path)
    store[name] = {
        "steps": steps,
        "match_field": match_field,
        "variance_threshold_pct": variance_threshold_pct,
        "escalate_to": escalate_to,
    }
    save_json(store_path, store)


def run_reconciliation(store_path: Path, name: str, invoices: list[dict]) -> list[dict]:
    """Trainer Note: this function has NO hard-coded business rule about
    5% or PO numbers - it reads whatever was taught in teach_procedure()
    and applies it generically. That's what 'reuse the procedure
    automatically' means in practice."""
    store = load_json(store_path)
    procedure = store.get(name)
    if procedure is None:
        raise ValueError(f"No procedure named '{name}' has been taught yet.")

    threshold = procedure["variance_threshold_pct"]
    results = []
    for invoice in invoices:
        po_amount = invoice["po_amount"]
        invoice_amount = invoice["invoice_amount"]
        variance_pct = abs(invoice_amount - po_amount) / po_amount * 100
        flagged = variance_pct > threshold
        results.append(
            {
                "invoice_id": invoice["invoice_id"],
                "po_number": invoice[procedure["match_field"]],
                "variance_pct": round(variance_pct, 2),
                "flagged": flagged,
                "escalated_to": procedure["escalate_to"] if flagged else None,
            }
        )
    return results


def demo_procedural_memory(store_path: Path, invoices: list[dict]) -> None:
    """Demo 4 from the deck (Slide 18): teach the procedure once, then feed
    a brand-new invoice batch and confirm all three steps ran."""
    section("Demo 4: Procedural Memory Build")

    step(1, "Teach the procedure once, narrated")
    console.print(
        "[bold green]Trainer says:[/bold green] \"Here's how we reconcile vendor invoices "
        "against PO records: match by PO number, flag variances over 5%, "
        "escalate flagged items to the AP lead.\""
    )
    teach_procedure(
        store_path,
        name="invoice_reconciliation",
        steps=["match by PO number", "flag variances over 5%", "escalate flagged items to the AP lead"],
        match_field="po_number",
        variance_threshold_pct=5.0,
        escalate_to="AP lead",
    )

    step(2, "Confirm it's stored as procedural memory")
    stored = load_json(store_path)["invoice_reconciliation"]
    key_value_panel("Stored Procedure: invoice_reconciliation", stored)

    step(3, "Feed a new invoice batch (never seen before)")
    console.print(f"[dim]Reconciling {len(invoices)} invoices using the stored procedure only.[/dim]")
    results = run_reconciliation(store_path, "invoice_reconciliation", invoices)

    step(4, "Verify all 3 steps ran without re-explanation")
    for r in results:
        status = "[bold red]FLAGGED -> escalated[/bold red]" if r["flagged"] else "[green]OK[/green]"
        console.print(
            f"  {r['invoice_id']} (PO {r['po_number']}): variance {r['variance_pct']}% - {status}"
        )

    flagged_count = sum(1 for r in results if r["flagged"])
    console.print(
        f"[bold cyan]{flagged_count} invoice(s) flagged and escalated to the AP lead - "
        "teach once, reuse across every future run and every user.[/bold cyan]"
    )
