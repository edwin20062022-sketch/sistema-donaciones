param(
    [string]$TargetUrl = "http://host.docker.internal:8000"
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path "reports/zap" | Out-Null
docker run --rm --network host -v "${PWD}/reports/zap:/zap/wrk/:rw" zaproxy/zap-stable zap-api-scan.py `
    -t "${TargetUrl}/openapi.json" -f openapi -r zap-report.html -J zap-report.json

