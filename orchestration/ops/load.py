from dagster import op
import subprocess


@op
def load_raw_to_postgres():
    subprocess.run(
        ["python", "src/medi_tg_analytics/loading/load_raw_to_postgres.py"],
        check=True
    )
