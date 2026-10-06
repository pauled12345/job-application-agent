#!/usr/bin/env powershell
<#
.SYNOPSIS
    Push job-application-agent repo to GitHub after authenticating.
    Run this when you wake up - it will open browser for auth.
#>

cd "$env:USERPROFILE\job-hunt"

# Ensure gh is in PATH
$env:PATH += ";C:\Program Files\GitHub CLI\"

Write-Host "=== GitHub Authentication ===" -ForegroundColor Cyan
Write-Host "A browser window will open for GitHub device authorization." -ForegroundColor Yellow
Write-Host "If it doesn't open automatically, go to: https://github.com/login/device" -ForegroundColor Yellow

gh auth login --web

Write-Host "`n=== Creating & Pushing Repo ===" -ForegroundColor Cyan
gh repo create job-application-agent --private --source=. --push --description "Automated job hunting: email sender, Lever/Canonical form fillers, resume renderer, company verifier, 18 applications sent, 80+ African tech companies verified"

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host "Repo: https://github.com/pauled12345/job-application-agent" -ForegroundColor Green