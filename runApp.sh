#!/bin/bash
# Wechsel in das Verzeichnis, in dem sich das Shell-Skript befindet
cd "$(dirname "$0")"

# Vorhandene Log-Datei löschen, falls vorhanden
LOGFILE="errors.log"

if [ -f "$LOGFILE" ]; then
    rm "$LOGFILE"
fi

# Start der Anwendung
source .venv/bin/activate
.venv/bin/python3 ./App.py >> "$LOGFILE" 2>&1