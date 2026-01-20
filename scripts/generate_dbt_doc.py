#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

from medi_tg_analytics.core.project_root import get_project_root


def run_cmd(cmd: list[str], cwd: Path) -> None:
    """Run a shell command with UTF-8 encoding support."""
    # Force UTF-8 environment for dbt's Unicode symbols
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        subprocess.run(cmd, cwd=cwd, check=True, env=env)
    except subprocess.CalledProcessError as exc:
        print(f"❌ Command failed: {' '.join(cmd)}")
        sys.exit(exc.returncode)


def load_env():
    """Load environment variables from .env file."""
    root = get_project_root()
    env_path = root / ".env"

    if not env_path.exists():
        print(f"❌ .env file not found at {env_path}")
        sys.exit(1)

    load_dotenv(dotenv_path=env_path)
    print("✅ Environment variables loaded (DB credentials ready)")


def main():
    print("=" * 60)
    print("📖 dbt Documentation Portal: Generating & Serving")
    print("=" * 60)

    load_env()

    root = get_project_root()
    dbt_project_dir = root / "dbt" / "medical_warehouse"

    if not dbt_project_dir.exists():
        print(f"❌ dbt project directory not found: {dbt_project_dir}")
        sys.exit(1)

    try:
        # Step 1: Generate the static catalog.json and manifest.json
        print("\n🛠️ Step 1: Generating documentation files...")
        run_cmd(["dbt", "docs", "generate"], cwd=dbt_project_dir)

        # Step 2: Serve the documentation site
        print("\n🌐 Step 2: Launching dbt docs server...")
        print(">>> Access your documentation at: http://localhost:8080")
        print(">>> (Press Ctrl+C to stop the server)")

        run_cmd(
            ["dbt", "docs", "serve", "--port", "8080"],
            cwd=dbt_project_dir,
        )

    except KeyboardInterrupt:
        print("\n\n👋 Docs server stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
