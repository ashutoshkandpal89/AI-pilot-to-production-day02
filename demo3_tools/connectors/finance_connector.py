# ============================================================================
# MOCK FINANCE CONNECTOR (Slide 24: enterprise connectors - ERP data)
#
# What students will learn:
#   Connectors aren't just documents - they can reach structured business
#   data too (ERP orders, budget approvals). Same governance rule applies:
#   confirm it enforces the same permission model before production
#   (Slide 25).
#
# Why it matters:
#   demo4_grounded_agent reuses this connector to check whether each PO in
#   an invoice batch has budget approval - one more real signal folded
#   into the end-to-end grounded answer.
#
# Flow:
#   1. connect() simulates wiring up the connector
#   2. get_budget_approval() looks up one PO's approval status
# ============================================================================

from shared.console import console
from shared.mock_data import load_json


class FinanceConnector:
    """Trainer Note: kept deliberately simple - one lookup method over a
    JSON ledger. A real SAP/Dynamics connector would authenticate and
    query a live ERP system for the same shape of answer."""

    def __init__(self, data_path: str):
        self._ledger = load_json(data_path)

    def connect(self) -> None:
        console.print("[green]Connected to Finance ERP connector (mock ledger).[/green]")

    def get_budget_approval(self, po_number: str) -> dict:
        for record in self._ledger:
            if record["po_number"] == po_number:
                return record
        return {"po_number": po_number, "budget_approved": False, "approver": None}
