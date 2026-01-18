#!/usr/bin/env python
"""
Exporter module to dump all DBT marts to CSV files.
Place this in: medi_tg_analytics/utils/exporter.py
"""

import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from medi_tg_analytics.core.settings import settings


def main():
    # Load environment variables
    load_dotenv()

    # Output directory for CSVs (processed/marts)
    output_dir = Path(settings.paths.DATA["processed_dir"]) / "marts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # List of marts to export
    tables = [
        "raw_marts.dim_channels",
        "raw_marts.dim_dates",
        "raw_marts.fct_messages"
    ]

    print(f"🚀 Export started at {datetime.now()}")
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        for table in tables:
            # Read table into Pandas DataFrame
            df = pd.read_sql(f"SELECT * FROM {table}", conn)

            # Clean table name for CSV
            table_name = table.replace("raw_marts.", "")
            csv_file = output_dir / f"{table_name}.csv"

            # Export CSV
            df.to_csv(csv_file, index=False)
            print(f"✅ Exported {table} → {csv_file}")

    except Exception as e:
        print(f"❌ Error during export: {e}")
        raise

    finally:
        if 'conn' in locals():
            conn.close()
            print("🔌 Database connection closed.")

    print(f"🎉 Export completed at {datetime.now()}")
    print(f"📂 CSVs saved in {output_dir}")


if __name__ == "__main__":
    main()
