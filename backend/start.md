Command to start server
uvicorn chatapp.asgi:application --port 8000 --workers 4 --log-level debug --reload