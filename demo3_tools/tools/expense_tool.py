# ============================================================================
# EXPENSE TOOL (one of three tools registered into the mock MCP toolbox)
#
# What students will learn:
#   A "tool" is just a plain function with a name, a description, and
#   keywords - that's all Foundry's tool-search needs to find it later.
#
# Why it matters:
#   This is the exact tool used in Demo 5 (Slide 22): "look up an
#   employee's pending expense reports" without editing the agent's prompt.
#
# Flow: mcp_toolbox.py registers TOOL_DEFINITION, then calls run() when the
# agent decides this tool is relevant.
# ============================================================================

from shared.models import ToolDefinition
from shared.mock_data import load_json

TOOL_DEFINITION = ToolDefinition(
    tool_id="expense-lookup",
    name="Expense Lookup Tool",
    description="Looks up an employee's expense reports, optionally filtered by status.",
    keywords=["expense", "expenses", "reimbursement", "pending"],
)


def run(data_path: str, employee_name: str, status: str | None = None) -> str:
    """Trainer Note: this is the actual tool execution - deliberately a
    plain function so students can read the whole tool in one screen."""
    expenses = load_json(data_path)
    matches = [e for e in expenses if e["employee_name"] == employee_name]
    if status:
        matches = [e for e in matches if e["status"] == status]

    if not matches:
        return f"No matching expenses found for {employee_name}."

    lines = [f"- ${e['amount']:.2f} ({e['status']}): {e['description']}" for e in matches]
    return f"Expenses for {employee_name}:\n" + "\n".join(lines)
