# ============================================================================
# PERMISSION FILTER (Slide 7: "Permission-Aware Grounding: The Non-Negotiable")
#
# What students will learn:
#   Retrieval must resolve against the CALLING USER's real permissions, not
#   the agent's own service identity. Two users asking the same question
#   can - and should - get two different, both-correct answers.
#
# Why it matters:
#   A service-identity agent that ignores document-level permissions is a
#   data leak waiting to happen - the single most common enterprise pilot
#   failure (Slide 7).
#
# Architecture:
#   documents -> filter by document.allowed_departments vs user.department
#             -> only the visible subset is ever handed to the answer step
#
# Flow:
#   1. Take the full document set and a calling user
#   2. Split into visible / filtered-out
#   3. Return only the visible set, plus a record of what was filtered
#      (so the trace can show it transparently, never silently)
#
# Expected Output:
#   Finance user sees the runway/burn document; Sales user does not, and
#   sees the sales pipeline document instead - both answers are correct
#   for what that user is allowed to see.
# ============================================================================

from shared.console import console, section, step, user_prompt, agent_answer, denied
from shared.models import User, Document


def filter_documents_for_user(documents: list[dict], user: User) -> tuple[list[dict], list[str]]:
    """Trainer Note: this is the ONE function every retrieval path in this
    repo must pass through before an answer is generated. Skipping this
    step is exactly the failure mode Slide 7 warns about."""
    visible = []
    filtered_out = []
    for doc_dict in documents:
        doc = Document(**doc_dict)
        if doc.is_visible_to(user):
            visible.append(doc_dict)
        else:
            filtered_out.append(doc.doc_id)
    return visible, filtered_out


def answer_for_user(documents: list[dict], user: User, question: str) -> str:
    """Trainer Note: a deliberately simple 'answer generator' - it just
    stitches together the visible documents' content. In a real Foundry
    agent this stitching is done by the model; we keep it literal here so
    the permission effect is unmistakable on screen."""
    visible, _ = filter_documents_for_user(documents, user)

    keywords = ["runway", "burn", "pipeline"]
    relevant = []
    for doc in visible:
        content_lower = doc["content"].lower()
        if any(keyword in content_lower for keyword in keywords):
            relevant.append(doc)

    if not relevant:
        return "I don't have access to documents that answer this for your role."

    return "\n".join(f"- {d['title']}: {d['content']}" for d in relevant)


def demo_permission_aware_grounding(documents: list[dict], user_a: User, user_b: User) -> None:
    """Demo 2 from the deck (Slide 10): same question, two users, two
    different, both-correct answers."""
    section("Demo 2: Permission-Aware Grounding Demo")

    question = "What is our current runway and burn rate?"

    step(1, f"Sign in / impersonate {user_a.display_name} ({user_a.department.value})")
    user_prompt(user_a.display_name, question)
    answer_a = answer_for_user(documents, user_a, question)
    agent_answer(answer_a)

    step(2, f"Switch to {user_b.display_name} ({user_b.department.value})")
    user_prompt(user_b.display_name, question)
    answer_b = answer_for_user(documents, user_b, question)
    if "don't have access" in answer_b:
        denied(answer_b)
    else:
        agent_answer(answer_b)

    step(3, "Explain why these two answers differ")
    _, filtered_for_b = filter_documents_for_user(documents, user_b)
    console.print(
        f"[bold cyan]{user_a.display_name} ({user_a.department.value}) can see the finance runway "
        f"report. {user_b.display_name} ({user_b.department.value}) cannot - it was filtered "
        f"before the answer step ran. Filtered doc IDs for {user_b.display_name}: "
        f"{filtered_for_b}[/bold cyan]"
    )
