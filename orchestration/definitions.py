from dagster import Definitions

from orchestration.pipeline import medical_telegram_pipeline
from orchestration.schedules import daily_medical_telegram_pipeline

defs = Definitions(
    jobs=[medical_telegram_pipeline],
    schedules=[daily_medical_telegram_pipeline],
)
