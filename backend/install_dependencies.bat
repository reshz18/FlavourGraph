@echo off
echo =========================================
echo   Installing FlavorGraph Backend
echo   Dependencies
echo =========================================
echo.

REM Upgrade pip first
echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

REM Install all requirements
echo.
echo [2/3] Installing requirements...
pip install -r requirements.txt

REM Verify critical packages
echo.
echo [3/3] Verifying installations...
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import uvicorn; print('✓ Uvicorn installed')"
python -c "import networkx; print('✓ NetworkX installed')"
python -c "import httpx; print('✓ HTTPX installed')"
python -c "import fuzzywuzzy; print('✓ FuzzyWuzzy installed')"
python -c "import dotenv; print('✓ Python-dotenv installed')"

echo.
echo =========================================
echo   ✅ Installation Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Spoonacular API key
echo 2. Run: python run.py
echo.
pause
