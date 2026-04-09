@echo off
set GIT="C:\Program Files\Git\cmd\git.exe"
cd /d "%~dp0"
(
%GIT% config user.email "builder@example.com"
%GIT% config user.name "Website Builder"
%GIT% remote remove origin 2^>nul
%GIT% remote add origin https://github.com/phanmaikienhung/market-report.git
%GIT% add -A
%GIT% commit -m "fix: dark mode readability for pre/code blocks"
%GIT% push -f origin HEAD:gh-pages
%GIT% log --oneline -3
echo DONE_EXIT_%ERRORLEVEL%
) > _deploy.log 2>&1
