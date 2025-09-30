@echo off
echo ============================================
echo   🔧 FIXING AND RUNNING FLAVORGRAPH BACKEND
echo ============================================
echo.

echo [Step 1] Installing missing fuzzywuzzy module...
pip install fuzzywuzzy python-Levenshtein

echo.
echo [Step 2] Installing all other dependencies...
pip install fastapi uvicorn networkx httpx python-dotenv pydantic

echo.
echo [Step 3] Testing imports...
python -c "import fuzzywuzzy; print('✅ FuzzyWuzzy OK')" 2>nul
if errorlevel 1 (
    echo ❌ FuzzyWuzzy still missing. Installing again...
    pip install --force-reinstall fuzzywuzzy
)

echo.
echo [Step 4] Starting backend server...
echo ============================================
echo   🚀 STARTING SERVER ON http://localhost:8000
echo ============================================
echo.
python run.py
