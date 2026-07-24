# Demo 1: Grounding - Foundry IQ + Permission-Aware Retrieval

Maps to **Slides 5-10** in `Day2_Foundry_Grounding_Agents.pptx` and
**Demos 1 & 2** in `Day2_Trainer_Demo_Script.docx`.

## What This Demo Teaches

- **Static RAG vs. Foundry IQ** - one-shot lookup against a frozen index
  vs. retrieval as an iterative reasoning step that can re-query mid-task.
- **Permission-aware grounding** - retrieval resolves against the calling
  user's real permissions, never a shared service identity.
- **The four-stage architecture** from Slide 8: User Query → Reasoning-
  Driven Retrieval → Permission Filter → Grounded Answer.

## Architecture

```
documents.json
      |
      v
static_rag.py   -----> one keyword search, frozen snapshot, no re-query
foundry_iq.py   -----> splits question, searches iteratively, re-queries live data
permission_filter.py -> filters documents by user.department before any answer is built
```

Nothing here calls a real Azure AI Foundry endpoint. The Azure AI Foundry
SDK import is shown in `shared/__init__.py`'s comments as where a real
project would plug in Foundry IQ; this repo simulates the *behavior* in
plain Python so the mechanics are visible.

## How to Run

```bash
cd day2-grounding-agents
pip install -r requirements.txt
python demo1_grounding/main.py
```

## Expected Output

1. **Static RAG section** - one search result set, then a source edit that
   the frozen index does not notice.
2. **Foundry IQ section** - a retrieval trace table with 2+ steps, followed
   by an immediate, correct answer after a live source edit.
3. **Permission-aware grounding section** - Test User A (Finance) sees the
   runway/burn report; Test User B (Sales) is denied it and sees the sales
   pipeline document instead.

## Talking Points

- "Static RAG answers 'what's in the index.' Foundry IQ answers 'what do I
  actually need to know to finish this task.'" (Slide 6)
- The permission filter step is the one teams most often skip when racing
  to a demo (Slide 8 trainer note) - point at `permission_filter.py` and
  note it runs before every answer in this repo, not after.
- Governance callback: this same permission model reappears in
  `demo3_tools`'s SharePoint connector (Slide 25/26) - the two must match.

## Questions Students May Ask

- **"Does Foundry IQ always issue exactly 2 queries?"** No - `_split_into_subquestions`
  is hard-coded here for teaching clarity. In a real Foundry IQ agent, the
  model decides how many queries it needs and when to stop.
- **"What happens if a document has no `allowed_departments` match for
  anyone?"** It's simply never visible to any user - permission filtering
  fails closed, not open.
- **"Where would the real Azure AI Foundry SDK call go?"** Inside
  `foundry_iq.py`'s `foundry_iq_answer`, replacing `_live_search` and the
  hard-coded decomposition with a real Foundry IQ retrieval call.
