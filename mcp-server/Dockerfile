FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY mcp-server/pyproject.toml .
COPY mcp-server/main.py .

RUN uv pip install --system --no-cache-dir "mcp[cli]>=1.6.0"

CMD ["python", "main.py"]