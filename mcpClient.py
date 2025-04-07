import asyncio
import traceback
from mcp import ClientSession
from mcp.client.sse import sse_client


async def run():
    try:
        async with sse_client(url="http://localhost:8000/subapi/sse") as streams:
            async with ClientSession(*streams) as session:
                print("Session initialized")

                # List available tools
                print("Listing available tools...")
                tools = await asyncio.wait_for(session.list_tools(), timeout=5)
                print("Available tools:", tools)

                # Call a tool
                print("Calling the add tool...")
                result = await asyncio.wait_for(session.call_tool("add", arguments={"a": 4, "b": 5}), timeout=5)
                print("Result of add tool:", result.content[0].text)

                # List available resources
                print("Listing available resources...")
                resources = await asyncio.wait_for(session.list_resources(), timeout=5)
                print("Available resources:", resources)

                # Read a resource
                print("Reading static resource...")
                content = await asyncio.wait_for(session.read_resource("resource://some_static_resource"), timeout=5)
                print("Static resource content:", content.contents[0].text)

                # Read a greeting resource
                print("Reading greeting resource for 'yash'...")
                content = await asyncio.wait_for(session.read_resource("greeting://yash"), timeout=5)
                print("Greeting content:", content.contents[0].text)

                # List available prompts
                print("Listing available prompts...")
                prompts = await asyncio.wait_for(session.list_prompts(), timeout=5)
                print("Available prompts:", prompts)

                # Get a review code prompt
                print("Getting review code prompt...")
                prompt = await asyncio.wait_for(session.get_prompt(
                    "review_code", arguments={"code": "print(\"Hello world\")"}
                ), timeout=5)
                print("Review code prompt:", prompt)

                # Get a debug error prompt
                print("Getting debug error prompt...")
                prompt = await asyncio.wait_for(session.get_prompt(
                    "debug_error", arguments={"error": "SyntaxError: invalid syntax"}
                ), timeout=5)
                print("Debug error prompt:", prompt)

    except asyncio.TimeoutError:
        print("A timeout occurred. The operation took too long.")
    except Exception as e:
        print("An error occurred:", str(e))
        traceback.print_exc()  # Print the traceback for more details


if __name__ == "__main__":
    asyncio.run(run())
