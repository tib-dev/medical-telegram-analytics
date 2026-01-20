#!/usr/bin/env python
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import subprocess
from medi_tg_analytics.core.project_root import get_project_root


def run_db_load():
    # ------------------------------------------------------------------
    # Load .env from project root
    # ------------------------------------------------------------------
    root = get_project_root()
    load_dotenv(root / ".env")

    required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [v for v in required_vars if v not in os.environ]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")

    # ------------------------------------------------------------------
    # Paths & Environment Setup
    # ------------------------------------------------------------------
    LOG_DIR = root / "logs" / "loading"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = LOG_DIR / "load_to_postgres.log"

    # Force UTF-8 for subprocess to prevent UnicodeEncodeError on Windows
    env_vars = os.environ.copy()
    env_vars["PYTHONIOENCODING"] = "utf-8"
    env_vars["PYTHONUTF8"] = "1"

    # ------------------------------------------------------------------
    # Run raw data loader
    # ------------------------------------------------------------------
    print(f"--- Starting raw data load to PostgreSQL ---")
    print(f"Log file: {LOG_FILE}")

    try:
        # Using 'with' for the file ensures it closes even if the process fails
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            process = subprocess.Popen(
                [sys.executable, "-m", "medi_tg_analytics.loading.load_raw_to_postgres"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                env=env_vars
            )

            # Stream output to console and log file in real-time
            for line in process.stdout:
                # Use sys.stdout.buffer.write if you want to be extremely safe,
                # but standard print usually works if env vars are set.
                print(line, end="", flush=True)
                f.write(line)

            process.wait()

            if process.returncode != 0:
                print(
                    f"\n[ERROR] Data load exited with code {process.returncode}")
                sys.exit(process.returncode)

        print(f"\n[SUCCESS] Raw data load completed successfully!")

    except KeyboardInterrupt:
        print("\n[STOP] Process interrupted by user. Killing subprocess...")
        process.kill()
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL] An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_db_load()
