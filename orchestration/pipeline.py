from dagster import job

from orchestration.ops.scrape import scrape_telegram_data
from orchestration.ops.load import load_raw_to_postgres
from orchestration.ops.dbt import run_dbt_transformations
from orchestration.ops.yolo import run_yolo_enrichment


@job
def medical_telegram_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(start_after=scrape)
    transform = run_dbt_transformations(start_after=load)
    run_yolo_enrichment(start_after=transform)
