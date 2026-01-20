#!/usr/bin/env python
import sys
from pathlib import Path
import subprocess

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs" / "yolo"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "yolo_enrichment.log"

# ------------------------------------------------------------------
# Run YOLO enrichment
# ------------------------------------------------------------------
print("🚀 Starting YOLOv8 image detection...")

# Redirect stdout and stderr to the log file
with open(LOG_FILE, "a") as f:
    process = subprocess.Popen(
        [sys.executable, "-m", "medi_tg_analytics.enrichment.yolo_detect"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    # Stream output to both console and log file
    for line in process.stdout:
        print(line, end="")
        f.write(line)

    process.wait()
    if process.returncode != 0:
        print(f"❌ YOLO enrichment exited with code {process.returncode}")
        sys.exit(process.returncode)

print(f"✅ YOLO detection completed. Results saved to {LOG_FILE}")
