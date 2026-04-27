FROM python:3.11-slim

WORKDIR /app

COPY mcp-server/pyproject.toml .
COPY mcp-server/main.py .

RUN pip install --no-cache-dir .

CMD ["python", "main.py"]