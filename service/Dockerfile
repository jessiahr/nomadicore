from python:3.11-slim
workdir /app
copy requirements.txt requirements.txt
run pip install --no-cache-dir -r requirements.txt
copy . .
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]