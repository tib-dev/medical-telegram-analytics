#!/usr/bin/env python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import subprocess

# ------------------------------------------------------------------
# Load environment variables safely
# ------------------------------------------------------------------
env_path = Path(".env")
if not env_path.is_file():
    print("❌ .env file not found")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs" / "scraping"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "scraper.log"

# ------------------------------------------------------------------
# Run Telegram scraper
# ------------------------------------------------------------------
print("🟢 Starting Telegram scraping...")

# Redirect stdout and stderr to the log file
with open(LOG_FILE, "a") as f:
    process = subprocess.Popen(
        [sys.executable, "-m", "medi_tg_analytics.scraping.scraper"],
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
        print(f"❌ Scraper exited with code {process.returncode}")
        sys.exit(process.returncode)

print(f"✅ Scraping finished, logs saved to {LOG_FILE}")
