# main.py

from fastapi import FastAPI
from mcpServer import mcp  # Import the initialized FastMCP instance

app = FastAPI()

# Mount MCP server as a sub-application at /subapi
app.mount("/subapi", mcp.sse_app())  # MCP uses Server-Sent Events here


# ✅ Root route
@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


# ✅ Sub route
@app.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


# ✅ Optional: Route to test if subapi is live (outside MCP's mounted app)
@app.get("/subapi-test")
def read_subapi_test():
    return {"message": "Hello World from sub2 (FastAPI side)"}

