# ============================================================================
# MOCK SHAREPOINT CONNECTOR (Slide 24-26: Enterprise Connectors)
#
# What students will learn:
#   A connector is another retrieval path into enterprise data - and it
#   MUST resolve against the same per-user permission model as Foundry IQ,
#   not a shared service identity (Slide 25).
#
# Why it matters:
#   Demo 6 (Slide 26) is an explicit callback to Demo 2 (Slide 10): same
#   two test users, same permission behavior, proving the connector didn't
#   introduce a new leak.
#
# Architecture:
#   data/sharepoint_finance_library.json -> filtered by user.department,
#   exactly like permission_filter.py in demo1_grounding.
#
# Flow:
#   1. connect() simulates wiring up the connector, scoped to one library
#   2. query_as_user() only ever returns documents visible to that user
#
# Expected Output:
#   Test User A (Finance) receives the board deck; Test User B (Sales)
#   does not - identical shape to Demo 2's result.
# ============================================================================

from shared.console import console
from shared.models import User, Document
from shared.mock_data import load_json


class SharePointConnector:
    """Trainer Note: 'connecting' here just means pointing at one JSON file
    scoped to a library name - a real connector authenticates against
    SharePoint and enforces the same document-level ACLs shown here."""

    def __init__(self, data_path: str, library_name: str):
        self.library_name = library_name
        self._documents = load_json(data_path)

    def connect(self) -> None:
        console.print(
            f"[green]Connected to SharePoint site's '{self.library_name}' document library.[/green]"
        )

    def query_as_user(self, user: User, question: str) -> str:
        """Trainer Note: this permission check is the whole point of the
        governance callback - it must behave identically to
        demo1_grounding/permission_filter.py's filter_documents_for_user."""
        visible_docs = []
        for doc_dict in self._documents:
            doc = Document(doc_id=doc_dict["doc_id"], title=doc_dict["title"],
                            content=doc_dict["content"], allowed_departments=doc_dict["allowed_departments"])
            if doc.is_visible_to(user):
                visible_docs.append(doc)

        if not visible_docs:
            return f"{user.display_name} ({user.department.value}) has no access to matching documents."

        lines = [f"- {d.title}: {d.content}" for d in visible_docs]
        return f"Results for {user.display_name} ({user.department.value}):\n" + "\n".join(lines)
