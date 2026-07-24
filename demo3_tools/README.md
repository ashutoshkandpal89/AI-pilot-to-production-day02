# Demo 3: MCP Toolbox + Enterprise Connectors

Maps to **Slides 19-26** in `Day2_Foundry_Grounding_Agents.pptx` and
**Demos 5 & 6** in `Day2_Trainer_Demo_Script.docx`.

## What This Demo Teaches

- **Register once, discover at runtime** (Slide 20) - tools are registered
  centrally in a toolbox, then found via keyword tool-search at question
  time, so only relevant tools enter the prompt.
- **MCP is a standard, not a Foundry-specific feature** (Slide 21) - the
  same register/discover/execute shape works with any MCP-compatible host.
- **Enterprise connectors are a new permission surface** (Slide 25) - every
  connector must enforce the same per-user model as Foundry IQ.

## Architecture

```
tools/expense_tool.py     -> keywords: expense, expenses, reimbursement, pending
tools/employee_tool.py    -> keywords: employee, manager, department, directory
tools/currency_tool.py    -> keywords: currency, convert, exchange, fx
mcp_toolbox.py             -> register_tool() / discover_tools() / execute_tool()

connectors/sharepoint_connector.py -> permission-filtered document connector
connectors/finance_connector.py    -> ERP-style budget approval lookup
```

Flow shown on screen: **Register Tool -> Discover Tool -> Execute Tool ->
Connector Retrieval** (matches the spec's required demo sequence).

## How to Run

```bash
cd day2-grounding-agents
pip install -r requirements.txt
python demo3_tools/main.py
```

## Expected Output

1. **Demo 5 (toolbox)** - the expense tool is registered, tool-search finds
   exactly 1 matching tool for a question about pending expenses, and it
   runs without any agent prompt text being touched.
2. **Demo 6 (connector)** - Test User A (Finance) sees the Q2 board deck;
   Test User B (Sales) does not - identical shape to Demo 1's permission
   result, proving the connector didn't introduce a new leak.

## Talking Points

- Only ONE tool is discovered per question here on purpose - open
  `mcp_toolbox.py`'s `discover_tools()` and show it's a keyword filter over
  *registered* tools only, nothing implicit.
- "An agent with 200 tools wired directly into its prompt is slower, more
  expensive, and more error-prone than one that searches for the 3 it
  needs" (Slide 20) - register the other two tools live if there's time,
  and show discovery still returns exactly one per question.
- Explicit callback: "remember Test User A and B from Section 01?" (Slide
  26 trainer note) - pull up `demo1_grounding`'s permission result side by
  side if convenient.

## Questions Students May Ask

- **"Does tool-search use embeddings in a real Foundry project?"** Yes -
  this repo uses plain keyword matching for teaching clarity; a production
  Foundry toolbox uses semantic search over tool descriptions.
- **"What's the difference between a Toolbox and MCP itself?"** MCP is the
  protocol a tool speaks (Slide 21); the Toolbox is Foundry's enterprise
  layer on top - centralized registration, versioning, and access control
  for which tools an agent is allowed to discover.
- **"Why does the Finance connector return `budget_approved: false` for
  one PO?"** That's intentional mock data (`data/finance_ledger.json`) -
  it's reused in `demo4_grounded_agent` to show a real, non-trivial signal
  feeding into the final approve/deny answer.
