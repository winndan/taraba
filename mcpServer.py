# server.py
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP app
mcp = FastMCP("Demo")


# Add tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


# Add resources
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"


# Expose mcp instance for import
__all__ = ["mcp"]
