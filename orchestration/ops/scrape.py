from dagster import op
import subprocess


@op
def scrape_telegram_data():
    subprocess.run(
        ["bash", "scripts/run_scraper.sh"],
        check=True
    )
