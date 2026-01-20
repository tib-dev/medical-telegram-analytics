from dagster import op, In, Nothing, OpExecutionContext
from medi_tg_analytics.core.project_root import get_project_root
from medi_tg_analytics.core.settings import settings
import subprocess
import sys
import os

root = get_project_root()
logs_dir = settings.paths.LOGS["dagster_logs_dir"]
logs_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# LOAD RAW DATA TO POSTGRES
# -------------------------------------------------------


@op(ins={"start": In(Nothing)})
def load_raw_to_postgres(context: OpExecutionContext):
    """
    Load scraped raw Telegram JSON data into PostgreSQL.
    """
    log_file = logs_dir / "load_to_postgres.log"
    script_path = root / "src/medi_tg_analytics/loading/load_raw_to_postgres.py"

    context.log.info(f"Running raw data loader: {script_path}")
    context.log.info(f"Loader logs -> {log_file}")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    with open(log_file, "a", encoding="utf-8") as f:
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            env=env,
        )

        for line in process.stdout:
            print(line, end="", flush=True)
            f.write(line)

        process.wait()
        if process.returncode != 0:
            context.log.error(f"Loader exited with code {process.returncode}")
            raise subprocess.CalledProcessError(
                process.returncode, process.args)

    context.log.info("Raw data loaded into PostgreSQL successfully")

