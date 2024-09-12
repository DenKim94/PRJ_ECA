#!/bin/bash
# Wechsel in das Verzeichnis, in dem sich das Shell-Skript befindet
cd "$(dirname "$0")"

# Start der Anwendung
source .venv/bin/activate
.venv/bin/python3 App.py