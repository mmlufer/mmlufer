from mcp.server.fastmcp import FastMCP

# Crear un servidor MCP
mcp = FastMCP("Calculadora")

@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números"""
    return a + b

@mcp.resource("saludo://{nombre}")
def obtener_saludo(nombre: str) -> str:
    """Obtiene un saludo personalizado"""
    return f"¡Hola, {nombre}!"

if __name__ == "__main__":
    mcp.run()
