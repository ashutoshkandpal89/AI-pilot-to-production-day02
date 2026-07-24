# ============================================================================
# EMPLOYEE TOOL (one of three tools registered into the mock MCP toolbox)
#
# What students will learn:
#   Same pattern as expense_tool.py - a description and keywords are all
#   that's needed for tool-search to discover this tool at runtime.
#
# Why it matters:
#   Shows students that adding a SECOND tool doesn't require touching the
#   first one, or the agent's prompt - each tool is fully independent.
# ============================================================================

from shared.models import ToolDefinition
from shared.mock_data import load_json

TOOL_DEFINITION = ToolDefinition(
    tool_id="employee-lookup",
    name="Employee Lookup Tool",
    description="Looks up an employee's department and manager from the directory.",
    keywords=["employee", "manager", "department", "directory"],
)


def run(data_path: str, employee_name: str) -> str:
    employees = load_json(data_path)
    for emp in employees:
        if emp["name"] == employee_name:
            return f"{emp['name']} - department: {emp['department']}, manager: {emp['manager']}"
    return f"No employee record found for {employee_name}."
