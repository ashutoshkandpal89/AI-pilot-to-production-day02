# ============================================================================
# DEMO 3: MCP TOOLBOX + ENTERPRISE CONNECTORS
#
# What students will learn:
#   - Register Once, Discover at Runtime (Slide 20) via a mock MCP toolbox
#   - Enterprise connectors reach governed data (Slide 24) and must enforce
#     the SAME permission model as Foundry IQ (Slide 25)
#
# Why it matters:
#   This section is about breadth and governance, not depth on any one
#   connector (Slide 23 trainer note).
#
# Architecture:
#   mcp_toolbox.py         -> register / discover / execute over 3 tools
#   connectors/sharepoint_connector.py -> permission-aware document connector
#   connectors/finance_connector.py    -> ERP-style structured data connector
#
# Flow: run this file directly. It walks Demo 5 (toolbox) then Demo 6
# (connector), explicitly calling back to Demo 2's permission result.
#
# Expected Output:
#   A tool-search trace showing exactly one tool discovered and executed,
#   followed by a two-user SharePoint comparison matching Demo 1's result.
# ============================================================================

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.console import console, section, step
from shared.config import print_mode_banner
from shared.mock_data import TEST_USER_A_FINANCE, TEST_USER_B_SALES
from mcp_toolbox import MCPToolbox, demo_toolbox_registration
from connectors.sharepoint_connector import SharePointConnector

DATA_DIR = Path(__file__).parent / "data"


def demo_connector_callback() -> None:
    """Demo 6 from the deck (Slide 26): wire up SharePoint live and show it
    respects the same permission model demonstrated with Foundry IQ."""
    section("Demo 6: Connecting to a Live Enterprise Connector")

    connector = SharePointConnector(
        data_path=str(DATA_DIR / "sharepoint_finance_library.json"),
        library_name="Finance",
    )

    step(1, "Add the SharePoint connector")
    connector.connect()

    step(2, "Scope it to the Finance library (already done at construction)")
    console.print("[dim]Connector is scoped to the 'Finance' document library only.[/dim]")

    step(3, "Ask as Test User A (Finance)")
    result_a = connector.query_as_user(TEST_USER_A_FINANCE, "last quarter's board deck")
    console.print(result_a)

    step(4, "Ask as Test User B (Sales), compare results")
    result_b = connector.query_as_user(TEST_USER_B_SALES, "last quarter's board deck")
    console.print(result_b)

    console.print(
        "[bold cyan]Remember Test User A and B from Foundry IQ earlier? Same result "
        "here - the connector didn't introduce a new leak.[/bold cyan]"
    )


def main() -> None:
    console.rule("[bold]DEMO 3: MCP TOOLBOX + ENTERPRISE CONNECTORS[/bold]")
    print_mode_banner()

    toolbox = MCPToolbox()
    demo_toolbox_registration(toolbox, expense_data_path=str(DATA_DIR / "expenses.json"))

    demo_connector_callback()

    section("Demo 3 complete")
    console.print(
        "[bold green]Recap:[/bold green] Toolbox = register once, discover at runtime. "
        "Connectors = a new permission surface every time - verify it enforces the "
        "same model as Foundry IQ before production."
    )


if __name__ == "__main__":
    main()
