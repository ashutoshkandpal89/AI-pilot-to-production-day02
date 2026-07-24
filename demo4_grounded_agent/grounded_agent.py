# ============================================================================
# COMPLETE ENTERPRISE GROUNDED AGENT (Slide 27-28: the climax)
#
# What students will learn:
#   Every pattern from today combined into ONE live answer: grounding,
#   permission enforcement, procedural memory, and tool/connector use.
#
# Why it matters:
#   "An agent that reasons well but fails any one of the checklist's three
#   questions isn't grounded - it's confidently guessing with better
#   vocabulary." (Slide 27)
#
# Architecture (this file wires together, does not reimplement):
#   demo1_grounding.permission_filter -> permission gate on the calling user
#   demo3_tools.connectors.sharepoint_connector -> expense policy lookup
#   demo2_memory.procedural_memory   -> taught invoice reconciliation
#   demo3_tools.connectors.finance_connector -> per-PO budget approval
#   demo3_tools.mcp_toolbox + tools.expense_tool -> discovered tool call
#
# Flow: run_grounded_query() runs all five stages in order and returns a
# single GroundedAnswer with every stage's result attached, so main.py can
# print each one exactly as it happened.
#
# Expected Output:
#   Finance/AP users get a full reconciliation verdict with sources,
#   procedure, and tool trace. A Sales user is stopped at the permission
#   gate before any financial data is touched.
# ============================================================================

import sys
from pathlib import Path
from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parent.parent
for path in (REPO_ROOT, REPO_ROOT / "demo1_grounding", REPO_ROOT / "demo2_memory", REPO_ROOT / "demo3_tools"):
    sys.path.insert(0, str(path))

from shared.models import User, Department
from shared.mock_data import load_json
from procedural_memory import teach_procedure, run_reconciliation
from mcp_toolbox import MCPToolbox
from connectors.sharepoint_connector import SharePointConnector
from connectors.finance_connector import FinanceConnector
from tools.expense_tool import TOOL_DEFINITION as expense_tool_def, run as expense_tool_run

DEMO1_DATA = REPO_ROOT / "demo1_grounding" / "data"
DEMO2_DATA = REPO_ROOT / "demo2_memory" / "data"
DEMO3_DATA = REPO_ROOT / "demo3_tools" / "data"
DEMO4_DATA = REPO_ROOT / "demo4_grounded_agent" / "data"

PROCEDURE_NAME = "invoice_reconciliation"


class GroundedAnswer(BaseModel):
    """Everything the final answer needs to show its work: sources,
    permission trace, procedure used, tool trace, and the verdict."""
    permitted: bool
    sources_used: list[str] = []
    policy_snippet: str | None = None
    procedure_used: str | None = None
    tool_trace: str | None = None
    reconciliation_results: list[dict] = []
    verdict: str


def _ensure_procedure_taught() -> None:
    """Trainer Note: reuses the EXACT same taught procedure from
    demo2_memory - nothing is re-derived here, only re-applied."""
    teach_procedure(
        DEMO4_DATA / "procedural_memory.json",
        name=PROCEDURE_NAME,
        steps=["match by PO number", "flag variances over 5%", "escalate flagged items to the AP lead"],
        match_field="po_number",
        variance_threshold_pct=5.0,
        escalate_to="AP lead",
    )


def run_grounded_query(user: User) -> GroundedAnswer:
    """Runs the full stack for one calling user and returns a GroundedAnswer.
    This is the single function demo4's main.py calls twice: once as
    Test User A (Finance) and once as Test User B (Sales)."""

    # Stage 1: Permission gate - resolves against the CALLING USER, not a
    # service identity. This must run before any financial data is touched.
    if user.department not in (Department.FINANCE, Department.AP):
        return GroundedAnswer(
            permitted=False,
            verdict=f"Access denied: {user.display_name} ({user.department.value}) is not "
                     f"authorized to run invoice reconciliation.",
        )

    sources_used = []

    # Stage 2: Grounding via the SharePoint connector - expense policy doc.
    sharepoint = SharePointConnector(str(DEMO3_DATA / "sharepoint_finance_library.json"), "Finance")
    policy_result = sharepoint.query_as_user(user, "expense policy")
    sources_used.append("SharePoint Finance library: Expense Policy 2026")

    # Stage 3: Procedural memory - teach once (idempotent), then apply.
    _ensure_procedure_taught()
    invoices = load_json(DEMO2_DATA / "invoice_batch.json")
    reconciliation_results = run_reconciliation(DEMO4_DATA / "procedural_memory.json", PROCEDURE_NAME, invoices)
    sources_used.append("Procedural memory: invoice_reconciliation")

    # Stage 4: Enterprise connector - Finance ERP budget approval per PO.
    finance = FinanceConnector(str(DEMO3_DATA / "finance_ledger.json"))
    for r in reconciliation_results:
        approval = finance.get_budget_approval(r["po_number"])
        r["budget_approved"] = approval["budget_approved"]
    sources_used.append("Finance connector: budget approval ledger")

    # Stage 5: Tool discovery - the expense-lookup tool, registered fresh
    # here to prove discovery works the same way as in demo3_tools.
    toolbox = MCPToolbox()
    toolbox.register_tool(expense_tool_def, lambda **kw: expense_tool_run(str(DEMO3_DATA / "expenses.json"), **kw))
    discovered = toolbox.discover_tools("check the AP lead's related pending expense reports")
    tool_trace = None
    if discovered:
        tool_trace = toolbox.execute_tool(discovered[0].tool_id, employee_name="Priya Nair", status="pending")

    # Final verdict: not ready if any flagged item lacks budget approval.
    blocking = [r for r in reconciliation_results if r["flagged"] and not r["budget_approved"]]
    if blocking:
        po_list = ", ".join(r["po_number"] for r in blocking)
        verdict = f"NOT ready to approve - {len(blocking)} flagged item(s) lack budget approval: {po_list}."
    else:
        verdict = "Ready to approve - all flagged variances already have budget approval on file."

    return GroundedAnswer(
        permitted=True,
        sources_used=sources_used,
        policy_snippet=policy_result,
        procedure_used=PROCEDURE_NAME,
        tool_trace=tool_trace,
        reconciliation_results=reconciliation_results,
        verdict=verdict,
    )
