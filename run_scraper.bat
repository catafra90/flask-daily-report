@echo off
cd /d %~dp0
call env\Scripts\activate
python scrape_clients.py
pause
