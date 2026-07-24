# ============================================================================
# SESSION MEMORY (Slide 13: "The One Everyone Already Has")
#
# What students will learn:
#   Session memory is scoped to a single conversation. It solves "remember
#   what I said three turns ago" - and nothing more. It does NOT persist to
#   a new session.
#
# Why it matters:
#   Table stakes, not a feature to sell (Slide 13 trainer note). We include
#   it mainly as the bottom rung of the memory ladder, to contrast against
#   user memory and procedural memory below.
#
# Architecture:
#   A plain Python dict, held in RAM for the lifetime of one SessionMemory
#   instance. Nothing is written to disk - that's the whole point.
#
# Flow:
#   1. Create a SessionMemory for this conversation
#   2. remember() stores a turn
#   3. recall() reads it back - only within THIS instance
#
# Expected Output:
#   A brand-new SessionMemory instance has no knowledge of a previous
#   instance's turns, proving the "one conversation" scope boundary.
# ============================================================================

from shared.console import console


class SessionMemory:
    """Trainer Note: one instance = one conversation. Create a new
    instance to prove scope - that's exactly what demo_session_scope()
    below does."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self._turns: list[str] = []

    def remember(self, turn_text: str) -> None:
        self._turns.append(turn_text)

    def recall_all(self) -> list[str]:
        return list(self._turns)


def demo_session_scope() -> None:
    """Trainer Note: proves session memory does NOT cross session
    boundaries - a fresh instance starts with zero knowledge."""
    session_1 = SessionMemory(session_id="session-1")
    session_1.remember("User said their budget question was about Q3.")

    console.print(f"[dim]Session 1 turns so far: {session_1.recall_all()}[/dim]")

    session_2 = SessionMemory(session_id="session-2")
    console.print(f"[dim]Session 2 (brand new) turns so far: {session_2.recall_all()}[/dim]")
    console.print(
        "[bold red]Session memory does not carry over - session_2 knows nothing "
        "about session_1. That's the boundary user memory exists to cross.[/bold red]"
    )
