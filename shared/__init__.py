# Trainer Note:
# This package holds the small set of building blocks every demo reuses:
# data models (shared/models.py), console/print helpers (shared/console.py),
# and the mock enterprise dataset (shared/mock_data.py).
#
# Nothing in here is Foundry-specific. In a real Azure AI Foundry project,
# these responsibilities are handled by the platform (Foundry IQ, Agent
# Service, Memory API). We simulate them here so the AUDIENCE can see the
# mechanics happen, in plain Python, on a live console.
