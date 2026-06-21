#!/usr/bin/env python3

import subprocess
import sys
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LCSC_FILE = SCRIPT_DIR / "lcsc.txt"
OUTPUT_DIR = SCRIPT_DIR

if not LCSC_FILE.exists():
    sys.exit(1)

with open(LCSC_FILE, "r", encoding="utf-8") as f:
    raw_lines = [
        line.strip()
        for line in f
        if line.strip() and not line.strip().startswith("#")
    ]

# Extract C-number only (handles "C1234567 (description)")
parts = []
for line in raw_lines:
    match = re.search(r"C\d+", line)
    if match:
        parts.append(match.group(0))

ok = True

for part in parts:
    # skip if already present
    if any(OUTPUT_DIR.glob(f"{part}*")):
        continue

    print(f"fetch {part}")

    cmd = [
        "easyeda2kicad",
        "--full",
        f"--lcsc_id={part}",
        "--output",
        str(OUTPUT_DIR),
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"success {part}")
    except subprocess.CalledProcessError:
        ok = False
        continue

if ok:
    print("done")