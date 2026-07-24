# Day 2: Grounding Agents in Enterprise Context

A teaching repository for the 90-minute Microsoft webinar **"Grounding
Agents in Enterprise Context: Foundry IQ, Memory & Tools"** - Day 2 of the
Advanced Practitioner Series.

Built from, and closely following:
- `Day2_Foundry_Grounding_Agents.pptx` (32 slides, the authoritative spec)
- `Day2_Trainer_Demo_Script.docx` (run of show, talk track, full demo scripts)

## This Is a Teaching Repo, Not a Production One

Every "Azure service" here (Foundry IQ, MCP toolbox, SharePoint, Finance
ERP) is **mocked in plain Python and JSON files**. Nothing calls a real
Azure endpoint. The goal is that a student can open any file and read,
top to bottom, exactly what happens - no hidden abstractions, no SDK black
boxes. `shared/config.py` shows exactly where real Azure AI Foundry SDK
credentials would go if you pointed this at a live project instead.

## Repository Layout

```
day2-grounding-agents/
  README.md              <- you are here
  requirements.txt
  .env.example
  shared/                 <- models, console styling, mock data helpers, config
  demo1_grounding/         <- Slides 5-10  | Demos 1 & 2 (static vs. dynamic RAG, permissions)
  demo2_memory/            <- Slides 11-18 | Demos 3 & 4 (session, user, procedural memory)
  demo3_tools/             <- Slides 19-26 | Demos 5 & 6 (MCP toolbox, enterprise connectors)
  demo4_grounded_agent/    <- Slides 27-28 | Demo 7 (the climax - everything combined)
```

Each `demoN_*/README.md` has its own "What This Demo Teaches,"
"Architecture," "How to Run," "Expected Output," "Talking Points," and
"Questions Students May Ask" - read those before presenting that section.

## Setup

```bash
git clone <this-repo>
cd day2-grounding-agents
pip install -r requirements.txt
cp .env.example .env   # optional - no demo requires this to run
```

## Running the Demos

```bash
python demo1_grounding/main.py
python demo2_memory/main.py
python demo3_tools/main.py
python demo4_grounded_agent/main.py
```

Run them in order - `demo4_grounded_agent` narrates a callback to concepts
introduced in the first three, and reuses their exact stored procedure and
mock data rather than re-deriving anything.

## Tech Stack

- **Python** - plain functions and small classes throughout; no advanced
  language features, so every line is explainable live.
- **Rich** - all console output (`shared/console.py`) for readable,
  attractive live-demo output.
- **Pydantic** - `shared/models.py` defines the schema for every mock
  entity (User, Document, RetrievalTrace, ToolDefinition, MemoryRecord).
- **python-dotenv** - `shared/config.py` loads `.env` and reports whether
  real Foundry credentials are present, without ever requiring them.
- **JSON** - every mock dataset (`data/*.json` in each demo folder) is
  plain, inspectable JSON - open it mid-demo and show the audience exactly
  what the agent can and cannot see.

Deliberately **not** used: LangChain, CrewAI, AutoGen - every pattern here
is built from first principles so the mechanics are visible.

## Teaching Style

Every module opens with a comment block covering what students will
learn, why it matters, the architecture, the flow, and the expected
output - matching the structure of the slide deck's own demo slides.
Every function with a non-obvious design choice has a `# Trainer Note:`
explaining the reasoning, in the same voice as the deck's own trainer
notes and the demo script's narration cues.

## Mapping to the Original 7-Demo Script

The trainer script lists 7 live demos; this repo's 4-folder structure
combines them as follows:

| Repo folder | Deck demo(s) | Slide(s) |
|---|---|---|
| `demo1_grounding` | Demo 1 (Dynamic Retrieval) + Demo 2 (Permission-Aware Grounding) | 9-10 |
| `demo2_memory` | Demo 3 (Session + User Memory) + Demo 4 (Procedural Memory) | 17-18 |
| `demo3_tools` | Demo 5 (Toolbox + MCP) + Demo 6 (Enterprise Connector) | 22, 26 |
| `demo4_grounded_agent` | Demo 7 (Climax: End-to-End) | 28 |
