FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY mcp-server/pyproject.toml .
COPY mcp-server/main.py .

# Generar requirements.txt desde el pyproject.toml e instalar
RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]