# Trainer Note:
# These are the two test identities from the deck's Demo 2 ("Test User A -
# Finance" / "Test User B - Sales"), reused in Demo 3's connector callback
# and Demo 4's end-to-end run. Keeping them in one place means every demo
# tells a consistent story about the same two people.

import json
from pathlib import Path

from shared.models import User, Department

TEST_USER_A_FINANCE = User(user_id="u-001", display_name="Test User A", department=Department.FINANCE)
TEST_USER_B_SALES = User(user_id="u-002", display_name="Test User B", department=Department.SALES)
AP_LEAD = User(user_id="u-003", display_name="AP Lead", department=Department.AP)


def load_json(path: str | Path) -> dict | list:
    """Trainer Note: every demo's 'documents', 'tools', and 'memory store'
    are plain JSON files under that demo's data/ folder. This keeps the
    mock enterprise data inspectable - open the .json file mid-demo and
    show the audience exactly what the agent can and can't see."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str | Path, data: dict | list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
