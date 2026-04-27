"""
FelipedelosH
2026

"""
# main.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RappiDemo")

@mcp.tool()
def saludar(nombre: str = "mundo") -> str:
    """Saluda a una persona."""
    return f"¡Hola, {nombre}!"

if __name__ == "__main__":
    # Transporte STDIO: permite a Claude Desktop hablar con este proceso
    mcp.run(transport="stdio")
