# Regenerate pytest HTML report and coverage (Report/09 workflow).
# Windows: report/ and Report/ are the same folder — output uses Report/pytest_report.html.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Error "Missing .venv. Run: python -m venv .venv; pip install -r requirements-dev.txt"
}

& $Python -m pytest tests/ -v `
    --html=Report/pytest_report.html `
    --self-contained-html `
    --cov=boundary `
    --cov=control `
    --cov=entity `
    --cov-report=html:htmlcov `
    --cov-report=term-missing

Write-Host ""
Write-Host "HTML report: Report/pytest_report.html"
Write-Host "Coverage:    htmlcov/index.html"
Write-Host "(Report/pytest_report.html is gitignored — refresh browser after run.)"
