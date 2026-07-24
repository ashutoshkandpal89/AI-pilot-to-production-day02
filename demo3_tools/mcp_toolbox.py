# ============================================================================
# MCP TOOLBOX (Slide 20: "Register Once, Discover at Runtime")
#
# What students will learn:
#   Toolbox = Tool-Search = Context Control. Tools are registered once,
#   centrally, then discovered by keyword search at question time - only
#   the relevant tool ever enters the prompt, not all of them.
#
# Why it matters:
#   Demo 5 (Slide 22): register a new tool once via its MCP definition and
#   prove the agent finds it without the agent's prompt ever being edited.
#
# Architecture (Slide 20, narrated left to right):
#   Toolbox -> Tool-Search -> Context Control
#
# Flow:
#   1. register_tool() adds a ToolDefinition + its callable to the toolbox
#   2. discover_tools() runs a keyword search over registered tools only
#   3. execute_tool() calls the ONE tool discovery selected
#
# Expected Output:
#   Registering a tool never touches any other tool's entry or any agent
#   prompt text; discovery for a given question returns exactly the tools
#   whose keywords match, nothing more.
# ============================================================================

from typing import Callable

from shared.console import console, section, step
from shared.models import ToolDefinition


class MCPToolbox:
    """Trainer Note: this whole class is the 'MCP server' for this demo -
    a registry mapping tool_id -> (ToolDefinition, callable). A real MCP
    server exposes the same register/discover/execute shape over the
    network; here it's local so students can read every line."""

    def __init__(self):
        self._tools: dict[str, tuple[ToolDefinition, Callable]] = {}

    def register_tool(self, definition: ToolDefinition, handler: Callable) -> None:
        console.print(f"[green]Registered tool:[/green] {definition.name} ({definition.tool_id})")
        self._tools[definition.tool_id] = (definition, handler)

    def discover_tools(self, question: str) -> list[ToolDefinition]:
        """Trainer Note: this is tool-search. It only looks at keywords on
        REGISTERED tools - a tool that was never registered can never be
        discovered, no matter how well it would answer the question."""
        question_lower = question.lower()
        found = []
        for definition, _handler in self._tools.values():
            if any(keyword in question_lower for keyword in definition.keywords):
                found.append(definition)
        return found

    def execute_tool(self, tool_id: str, **kwargs) -> str:
        if tool_id not in self._tools:
            raise ValueError(f"Tool '{tool_id}' is not registered.")
        _definition, handler = self._tools[tool_id]
        return handler(**kwargs)

    def registered_tool_ids(self) -> list[str]:
        return list(self._tools.keys())


def demo_toolbox_registration(toolbox: MCPToolbox, expense_data_path: str) -> None:
    """Demo 5 from the deck (Slide 22): register a tool live, don't touch
    the agent's prompt, ask a question that needs it, show the trace."""
    from tools.expense_tool import TOOL_DEFINITION as expense_def, run as expense_run

    section("Demo 5: Toolbox + MCP Registration Walkthrough")

    step(1, "Register the expense-lookup tool in the toolbox via its MCP server definition")
    toolbox.register_tool(expense_def, lambda **kw: expense_run(expense_data_path, **kw))

    step(2, "Do NOT touch the agent's prompt")
    console.print(
        "[dim]Agent instructions file: unchanged before and after registration - "
        "no edits were made.[/dim]"
    )

    step(3, "Ask a question that needs this tool")
    question = "Find and use whatever tool helps look up an employee's pending expense reports."
    console.print(f'[bold green]Question:[/bold green] "{question}"')

    step(4, "Show the tool-search trace")
    discovered = toolbox.discover_tools(question)
    console.print(f"[bold]Tool-search discovered {len(discovered)} tool(s):[/bold]")
    for d in discovered:
        console.print(f"  - {d.name} ({d.tool_id})")

    if discovered:
        result = toolbox.execute_tool(discovered[0].tool_id, employee_name="Dana Reyes", status="pending")
        console.print(f"[bold magenta]Tool output:[/bold magenta]\n{result}")

    console.print(
        "[bold cyan]Zero prompt engineering was needed to make the new tool usable - "
        "that's the entire register-once-discover-at-runtime pitch.[/bold cyan]"
    )
