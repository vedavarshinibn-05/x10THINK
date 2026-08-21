@echo off
echo.
echo  ====================================================
echo   X10THINK - AI Agriculture Land Intelligence
echo  ====================================================
echo.
echo  Starting Backend (FastAPI on port 8000)...
start cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak > nul
echo  Backend started!
echo.
echo  Starting Frontend (React on port 5173)...
start cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 4 /nobreak > nul
echo  Frontend started!
echo.
echo  ====================================================
echo   Open http://localhost:5173 in your browser
echo  ====================================================
echo.
start http://localhost:5173
pause
