from fasthtml.common import *
from mcpServer import mcp  # Import the initialized FastMCP instance


app = FastHTML(routes=[
        Mount('/subapi', app=mcp.sse_app()),
    ])

#app.mount("/subapi", mcp.sse_app()) 

# ✅ Root route
@app.get("/")
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

serve()