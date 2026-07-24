# Trainer Note:
# Pydantic models are the "shape" of our simulated Foundry platform.
# We use them everywhere instead of raw dicts so that:
#   1. Every demo's data is self-documenting (open this file, see the whole schema)
#   2. Typos get caught immediately with a validation error, live, on screen
#   3. It mirrors how Azure AI Foundry SDK objects are typed in real projects
#
# Nothing here is advanced Python - just plain class definitions with type hints.

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Department(str, Enum):
    """Trainer Note: mirrors the Finance vs Sales split used in Demo 1's
    permission-aware grounding walkthrough and Demo 3's connector demo."""
    FINANCE = "finance"
    SALES = "sales"
    AP = "accounts_payable"


class User(BaseModel):
    """A calling user. Foundry IQ resolves retrieval against THIS identity,
    never against the agent's own service identity."""
    user_id: str
    display_name: str
    department: Department


class Document(BaseModel):
    """A single enterprise document in our mock knowledge source.
    allowed_departments models document-level permissions - the same
    concept as SharePoint/Foundry IQ ACLs, simplified to a list."""
    doc_id: str
    title: str
    content: str
    allowed_departments: list[Department]
    version: int = 1

    def is_visible_to(self, user: User) -> bool:
        return user.department in self.allowed_departments


class RetrievalStep(BaseModel):
    """One iteration of retrieval-as-reasoning. Foundry IQ can issue several
    of these inside a single answer - that's the point of Demo 1."""
    step_number: int
    query_issued: str
    docs_found: list[str] = Field(default_factory=list)
    reasoning: str


class RetrievalTrace(BaseModel):
    """The full trace shown to the audience after a grounded answer -
    every query issued, every document touched, and why."""
    steps: list[RetrievalStep] = Field(default_factory=list)
    docs_filtered_by_permission: list[str] = Field(default_factory=list)

    def add_step(self, query: str, docs_found: list[str], reasoning: str) -> None:
        self.steps.append(
            RetrievalStep(
                step_number=len(self.steps) + 1,
                query_issued=query,
                docs_found=docs_found,
                reasoning=reasoning,
            )
        )


class ToolDefinition(BaseModel):
    """A tool registered once in the mock MCP toolbox. Mirrors Demo 5:
    'register once, discover at runtime' rather than hard-coding tools
    into the agent's prompt."""
    tool_id: str
    name: str
    description: str
    keywords: list[str]


class ToolCallResult(BaseModel):
    tool_id: str
    success: bool
    output: str


class MemoryRecord(BaseModel):
    """A generic memory entry. scope distinguishes session / user /
    procedural memory - see demo2_memory for how each is used."""
    scope: str  # "session" | "user" | "procedural"
    key: str
    value: str
    owner_id: Optional[str] = None  # user_id for user memory, None for procedural
