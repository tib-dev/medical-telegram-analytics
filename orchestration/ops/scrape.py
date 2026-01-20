from dagster import op, In, Nothing, OpExecutionContext
from medi_tg_analytics.core.project_root import get_project_root
from medi_tg_analytics.core.settings import settings
import subprocess
import sys

root = get_project_root()
logs_dir = settings.paths.LOGS["dagster_logs_dir"]
logs_dir.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------
# SCRAPE TELEGRAM DATA
# -------------------------------------------------------
@op(ins={"start": In(Nothing)})
def scrape_telegram_data(context: OpExecutionContext):
    """
    Scrape raw Telegram data using the Python scraper module.
    """
    log_file = logs_dir / "scrape_telegram.log"
    script_path = root / "src/medi_tg_analytics/scraping/scraper.py" 

    context.log.info(f"Running Telegram scraper: {script_path}")
    context.log.info(f"Scraper logs -> {log_file}")

    with open(log_file, "a") as f:
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        for line in process.stdout:
            print(line, end="")
            f.write(line)
        process.wait()
        if process.returncode != 0:
            context.log.error(f"Scraper exited with code {process.returncode}")
            raise subprocess.CalledProcessError(
                process.returncode, process.args)

    context.log.info("Telegram scraping completed successfully")

