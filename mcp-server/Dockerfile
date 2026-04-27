FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de dependencias y código
COPY mcp-server/pyproject.toml .
COPY mcp-server/main.py .

# Instalar dependencias desde pyproject.toml
# (el punto . indica que instale el proyecto actual)
RUN pip install --no-cache-dir .

# El servidor se ejecutará en modo stdio (sin red)
CMD ["python", "main.py"]