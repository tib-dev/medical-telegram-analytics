#!/usr/bin/env bash

set -euo pipefail
trap 'echo "❌ Error on line $LINENO at command: $BASH_COMMAND"; exit 1' ERR

echo "===================================================="
echo "🚀 Exporting marts to CSV"
echo "===================================================="

# Change to project root if needed (optional)
# cd "$(dirname "$0")/../"

# Run the Python exporter module
python -m medi_tg_analytics.utils.exporter

echo "✅ Export completed successfully!"
echo "===================================================="
