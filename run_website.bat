@echo off
REM Start backend (if you use it) and a static frontend server with clean URLs.
REM This script will try to start the Flask backend and the frontend dev server.

REM Start backend in a new window (optional) if backend exists
if exist backend\app.py (
	start "Backend" cmd /k "cd backend && if exist venv\Scripts\activate (call venv\Scripts\activate) && python app.py"
) else (
	echo No backend found at backend\app.py, skipping backend.
)

REM Start frontend clean-URL server
start "Frontend" cmd /k "python serve.py 8000"

<<<<<<< HEAD
echo Backend available at http://localhost:5000
echo Frontend available at http://localhost:8000 (clean URLs enabled)
echo Both windows opening - press any key when ready to close...
=======
echo Frontend available at http://localhost:8000 (clean URLs enabled)
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
pause
