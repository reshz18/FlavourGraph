@echo off
echo Starting FlavorGraph Backend...
echo.
echo Installing dependencies if needed...
pip install fuzzywuzzy python-Levenshtein httpx fastapi uvicorn networkx python-dotenv

echo.
echo Starting server...
python run.py
pause
