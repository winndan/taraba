import asyncio
import logging
from mcp import ClientSession
from mcp.client.sse import sse_client
import httpx

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run():
    """Main asynchronous function to connect to the SSE endpoint and interact with the MCP API."""
    logger.info("Connecting to the SSE endpoint...")
    async with sse_client(url="http://localhost:8000/subapi/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            logger.info("✅ Session initialized. Session ID: %s", session.session_id)

            await list_tools(session)
            await call_tool(session)
            await list_resources(session)
            await read_resources(session)
            await list_prompts(session)
            await get_prompts(session)

            # Send a message to the FastAPI server
            message = "Hello from the MCP client!"
            logger.info("📤 Sending message: '%s' to session ID: %s", message, session.session_id)
            await send_message(session.session_id, message)

async def list_tools(session):
    """List available tools from the MCP API."""
    logger.debug("🔧 Listing available tools...")
    tools = await session.list_tools()
    logger.debug("Tools: %s", tools)

async def call_tool(session):
    """Call a specific tool from the MCP API."""
    logger.debug("🧠 Calling 'add' tool with arguments a=4, b=5...")
    result = await session.call_tool("add", arguments={"a": 4, "b": 5})
    logger.debug("Result of 'add': %s", result.content[0].text)

async def list_resources(session):
    """List available resources from the MCP API."""
    logger.debug("📦 Listing available resources...")
    resources = await session.list_resources()
    logger.debug("Available resources: %s", resources)

async def read_resources(session):
    """Read specific resources from the MCP API."""
    logger.debug("📄 Reading resource 'resource://some_static_resource'...")
    content = await session.read_resource("resource://some_static_resource")
    logger.debug("Static resource content: %s", content.contents[0].text)

    logger.debug("📄 Reading resource 'greeting://yash'...")
    content = await session.read_resource("greeting://yash")
    logger.debug("Greeting content: %s", content.contents[0].text)

async def list_prompts(session):
    """List available prompts from the MCP API."""
    logger.debug("💬 Listing available prompts...")
    prompts = await session.list_prompts()
    logger.debug("Available prompts: %s", prompts)

async def get_prompts(session):
    """Get specific prompts from the MCP API."""
    logger.debug("🔍 Getting prompt 'review_code'...")
    prompt = await session.get_prompt(
        "review_code", arguments={"code": 'print("Hello world")'}
    )
    logger.debug("Output from 'review_code': %s", prompt)

    logger.debug("🔍 Getting prompt 'debug_error'...")
    prompt = await session.get_prompt(
        "debug_error", arguments={"error": "SyntaxError: invalid syntax"}
    )
    logger.debug("Output from 'debug_error': %s", prompt)

async def send_message(session_id, message):
    """Send a message to the FastAPI server."""
    url = f"http://localhost:8000/messages?session_id={session_id}"
    payload = {"message": message}

    try:
        logger.debug("📡 Sending POST request to %s with payload: %s", url, payload)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, follow_redirects=False)
            logger.debug("Received response status: %s", response.status_code)
            if response.status_code in [200, 201, 202]:
                logger.info("✅ Message sent successfully.")
                response_data = response.json()
                logger.debug("Response data: %s", response_data)
            else:
                error_message = response.text
                logger.error("❌ Error sending message: %s - %s", response.status_code, error_message)
    except Exception as e:
        logger.exception("🔥 Exception while sending message: %s", e)

if __name__ == "__main__":
    asyncio.run(run())
