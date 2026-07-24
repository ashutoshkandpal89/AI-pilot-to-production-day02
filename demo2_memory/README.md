# Demo 2: Enterprise Memory - Session, User, and Procedural

Maps to **Slides 11-18** in `Day2_Foundry_Grounding_Agents.pptx` and
**Demos 3 & 4** in `Day2_Trainer_Demo_Script.docx`.

## What This Demo Teaches

- **The memory ladder** (Slide 12) - session (one conversation), user (one
  person, every future session), procedural (one task pattern, every user).
- **Session memory** is table stakes - it does not cross a session boundary.
- **User memory** persists preferences to disk and needs the same
  governance as any PII store (Slide 14).
- **Procedural memory** is taught once and reused automatically on data it
  has never seen - the highest-ROI memory type most pilots skip (Slide 15).

## Architecture

```
session_memory.py     -> in-RAM dict, dies with the process (one conversation)
user_memory.py         -> data/user_memory.json        (one user, many sessions)
procedural_memory.py   -> data/procedural_memory.json  (shared task pattern)
                        -> data/invoice_batch.json      (never-before-seen data to reconcile)
```

## How to Run

```bash
cd day2-grounding-agents
pip install -r requirements.txt
python demo2_memory/main.py
```

Re-run freely - `main.py` resets both JSON stores to empty at the start of
every run, so the "teach once" moment is genuine each time.

## Expected Output

1. **Session memory** - a second `SessionMemory` instance starts with zero
   knowledge of the first, proving the conversation-only scope.
2. **User memory (Demo 3)** - a formatting preference set once is applied
   automatically in a simulated new session, with no restatement.
3. **Procedural memory (Demo 4)** - the reconciliation procedure is taught
   once, then correctly flags 2 of 5 invoices on a batch it has never seen,
   using only the stored procedure.

## Talking Points

- "Default to session memory - it's free and already there" (Slide 16).
- User memory governance: point out it's a plain JSON file on purpose -
  open `data/user_memory.json` and ask "how would you apply a
  right-to-be-forgotten request to this file?"
- Procedural memory's `run_reconciliation()` has no hard-coded 5% or PO
  logic in it - it reads whatever `teach_procedure()` stored. That's the
  literal meaning of "teach once, reuse automatically."

## Questions Students May Ask

- **"Where would real Azure AI Foundry memory APIs plug in?"** They would
  replace the JSON read/write in `user_memory.py` and `procedural_memory.py`
  with calls to Foundry's memory store; the function signatures here are
  written to make that swap a drop-in.
- **"Why is procedural memory not scoped to a user?"** By design - Slide 15
  says it's "shared across users who perform it." Any user who invokes
  `run_reconciliation` gets the same taught procedure.
- **"What happens if you ask for a procedure that was never taught?"**
  `run_reconciliation` raises a clear `ValueError` - procedural memory
  fails loudly, not silently, when nothing has been taught yet.
