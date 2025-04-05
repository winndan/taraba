from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.sse import SseServerTransport
from mcpServer import mcp  # Your initialized MCP instance
import logging

app2 = FastAPI()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create SSE Transport for handling messages
sse = SseServerTransport("/messages")
server = mcp  # Your initialized MCP instance

# Mount the MCP server under /subapi
app2.mount("/subapi", app=server.sse_app())

@app2.get("/hello")
async def hello():
    """A simple endpoint for testing server response."""
    return {"message": "Hello from the main FastAPI app"}

# Endpoint to handle SSE connections at /subapi/sse
@app2.get("/subapi/sse")
async def handle_sse(request: Request):
    """Handle incoming SSE connections."""
    scope = request.scope
    receive = request.receive
    
    async with sse.connect_sse(scope, receive) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

# Endpoint to handle incoming messages
@app2.post("/messages")
@app2.post("/messages/")
async def handle_messages(request: Request):
    """Handle incoming messages for SSE."""
    logger.info("Received a message request.")
    
    # Debug request information
    logger.debug("Request URL: %s", request.url)
    logger.debug("Request query params: %s", request.query_params)
    
    # Check for session_id in query parameters
    session_id = request.query_params.get("session_id")
    if session_id is None or session_id == "{session_id}":
        logger.warning("Received invalid session ID: %s", session_id)
        return JSONResponse(status_code=400, content={"message": "Invalid session ID"})
    
    # Handle the message if session ID is valid
    try:
        logger.debug("Processing message with session ID: %s", session_id)
        
        # Get the request body
        body = await request.json()
        logger.debug("Received message body: %s", body)
        
        # Here you would typically integrate with your MCP server's logic
        # to handle the message and send any necessary responses back over SSE.
        
        logger.info("Message processed successfully.")
        return JSONResponse(content={"message": "Message received successfully", "session_id": session_id})
    except Exception as e:
        logger.exception("Error processing message: %s", e)
        return JSONResponse(status_code=500, content={"message": f"Server error: {str(e)}"})
