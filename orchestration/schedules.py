from dagster import schedule
from orchestration.pipeline import medical_telegram_pipeline


@schedule(
    cron_schedule="0 2 * * *",  # Daily at 02:00
    job=medical_telegram_pipeline,
    execution_timezone="Africa/Addis_Ababa",
)
def daily_medical_telegram_pipeline():
    return {}
