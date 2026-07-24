# Demo 4: Complete Enterprise Grounded Agent (The Climax)

Maps to **Slides 27-28** in `Day2_Foundry_Grounding_Agents.pptx` and
**Demo 7** in `Day2_Trainer_Demo_Script.docx`.

## What This Demo Teaches

Every pattern from the session combined into one live answer:

- **Grounding** - SharePoint connector retrieval (demo3_tools)
- **Permission** - calling-user gate before any financial data is touched (demo1_grounding)
- **Memory** - the exact procedure taught in demo2_memory, reused unchanged
- **Tool Discovery** - the expense-lookup tool, discovered via demo3_tools' toolbox
- **Enterprise Connector** - the Finance connector's budget-approval ledger

## Architecture

```
grounded_agent.py: run_grounded_query(user)
   |
   +-- Stage 1: permission gate (Finance/AP only)
   +-- Stage 2: SharePoint connector -> expense policy retrieval
   +-- Stage 3: procedural memory -> taught reconciliation, applied
   +-- Stage 4: Finance connector -> budget approval per PO
   +-- Stage 5: MCP toolbox -> discover + execute expense-lookup tool
   |
   -> GroundedAnswer (verdict, sources, procedure, tool trace)
```

This file imports directly from `demo1_grounding`, `demo2_memory`, and
`demo3_tools` - nothing here is reimplemented, only wired together, which
is the point: today's pieces compose.

## How to Run

```bash
cd day2-grounding-agents
pip install -r requirements.txt
python demo4_grounded_agent/main.py
```

Run `demo1_grounding`, `demo2_memory`, and `demo3_tools` first if you want
the audience to have already seen each piece individually before this
demo recombines them.

## Expected Output

1. The design checklist (Slide 27) printed before any query runs.
2. **Test User A (Finance)**: a full verdict - "NOT ready to approve" (one
   flagged invoice lacks budget approval), with sources, the taught
   procedure, and the expense-lookup tool trace all shown.
3. **Test User B (Sales)**: stopped at the permission gate before any
   financial data is touched or reconciliation runs at all.

## Talking Points

- This is the centerpiece - protect its time slot (Slide 28 trainer note).
- Point at `grounded_agent.py`'s five clearly-numbered stages and note
  each one is a straight import from an earlier demo - nothing new was
  written for the combination itself.
- The verdict differs from a "yes/no" answer - it names the exact blocking
  PO, because a real grounded agent should always be able to show its
  work, not just its conclusion.

## Questions Students May Ask

- **"Why does Test User A also get denied for parts of this in
  demo1_grounding but not here?"** Different question, different data -
  here the check is department-based (Finance/AP can run reconciliation),
  not document-level ACLs like Demo 1's runway report. Both are permission
  checks; they resolve against the same calling-user identity.
- **"What would change for a real Foundry deployment?"** Each of the five
  stages already isolates exactly what would be replaced: `foundry_iq`
  calls for retrieval, real Foundry IQ permission resolution, a real
  memory store, and real MCP/connector endpoints - the orchestration
  shape in `grounded_agent.py` stays the same.
- **"What happens if the procedure was never taught before this demo
  runs?"** It can't be - `_ensure_procedure_taught()` teaches it
  idempotently on every call, so this demo works standalone even if
  `demo2_memory` was never run first.
