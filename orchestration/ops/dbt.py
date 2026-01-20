from dagster import op
import subprocess


@op
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run"],
        cwd="dbt/medical_warehouse",
        check=True
    )

    subprocess.run(
        ["dbt", "test"],
        cwd="dbt/medical_warehouse",
        check=True
    )
