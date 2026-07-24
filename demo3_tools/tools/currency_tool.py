# ============================================================================
# CURRENCY TOOL (one of three tools registered into the mock MCP toolbox)
#
# What students will learn:
#   A third, unrelated tool - reinforces that tool-search only pulls in
#   the ONE relevant tool per question, not all three every time
#   (Slide 20: "an agent with 200 tools wired directly into its prompt").
#
# Why it matters:
#   Fixed mock exchange rates keep this demo fully offline - no external
#   API calls, no network dependency during a live session.
# ============================================================================

from shared.models import ToolDefinition

TOOL_DEFINITION = ToolDefinition(
    tool_id="currency-convert",
    name="Currency Conversion Tool",
    description="Converts an amount between currencies using fixed mock exchange rates.",
    keywords=["currency", "convert", "exchange", "fx"],
)

# Trainer Note: fixed rates, not a live FX feed - keeps this demo
# deterministic and network-free during a live session.
_MOCK_RATES = {
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.09,
    ("USD", "SGD"): 1.34,
    ("SGD", "USD"): 0.75,
}


def run(amount: float, from_currency: str, to_currency: str) -> str:
    if from_currency == to_currency:
        return f"{amount:.2f} {from_currency} = {amount:.2f} {to_currency} (same currency)"

    rate = _MOCK_RATES.get((from_currency, to_currency))
    if rate is None:
        return f"No mock exchange rate available for {from_currency} -> {to_currency}."

    converted = amount * rate
    return f"{amount:.2f} {from_currency} = {converted:.2f} {to_currency} (mock rate {rate})"
