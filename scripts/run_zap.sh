#!/usr/bin/env bash
set -euo pipefail

TARGET_URL="${1:-http://host.docker.internal:8000}"
mkdir -p reports/zap
docker run --rm --network host -v "$(pwd)/reports/zap:/zap/wrk/:rw" zaproxy/zap-stable zap-api-scan.py \
  -t "${TARGET_URL}/openapi.json" -f openapi -r zap-report.html -J zap-report.json

