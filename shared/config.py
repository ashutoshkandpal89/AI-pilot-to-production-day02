# Trainer Note:
# This file is the ONLY place in the repo that touches environment
# variables or the Azure AI Foundry SDK's connection details. Every demo
# runs in MOCK mode regardless of what's in .env - this exists so students
# see exactly where real credentials would go if this repo were pointed at
# a live Foundry project instead of local JSON files.

import os
from dotenv import load_dotenv

from shared.console import console

load_dotenv()  # reads .env in the repo root, if present


def print_mode_banner() -> None:
    """Trainer Note: call this once at the top of each demo's main(). It
    never changes what the demo does - the demos always run against mock
    data - it only tells the audience whether real Foundry credentials
    were detected in .env."""
    endpoint = os.getenv("AZURE_AI_FOUNDRY_PROJECT_ENDPOINT")
    if endpoint:
        console.print(f"[dim]Foundry project endpoint detected in .env: {endpoint} "
                       "(not used - this repo always runs on mock data).[/dim]")
    else:
        console.print(
            "[dim]No .env found / no Foundry endpoint set - running fully in MOCK "
            "mode on local JSON data (this is expected for this repo).[/dim]"
        )
