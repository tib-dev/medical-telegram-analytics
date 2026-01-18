#!/usr/bin/env bash

set -euo pipefail
trap 'echo "❌ Error on line $LINENO at command: $BASH_COMMAND"; exit 1' ERR

echo "===================================================="
echo "🚀 Running dbt models, tests, and generating docs"
echo "===================================================="

# Change to dbt project directory
DBT_PROJECT_DIR="$(dirname "$0")/../dbt/medical_warehouse"
cd "$DBT_PROJECT_DIR"

echo "✅ cleaning the history..."
dbt clean

echo "✅ Running dbt models..."
dbt run

echo "✅ Running dbt tests..."
dbt test

echo "✅ Generating dbt documentation..."
dbt docs generate

echo "✅ Launching dbt docs server..."
echo "Open the docs in your browser at http://localhost:8080"
dbt docs serve --port 8080

echo "===================================================="
echo "🎉 dbt pipeline completed"
echo "===================================================="
