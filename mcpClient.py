# mcpClient.py

from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio


async def run():
    print("🔌 Connecting to MCP server at http://localhost:8000/subapi/sse ...")

    try:
        # Establish SSE connection to the MCP server
        async with sse_client(url="http://localhost:8000/subapi/sse") as streams:
            async with ClientSession(*streams) as session:

                print("✅ Connected. Initializing session...")
                await session.initialize()

                # 🔍 List available tools
                tools = await session.list_tools()
                print("\n🛠 Available Tools:")
                for tool in tools:
                    print(f" - {tool.name}: {tool.description}")

                # ➕ Call the 'add' tool
                result = await session.call_tool("add", arguments={"a": 4, "b": 5})
                print("\n➕ Result of add(4, 5):", result.content[0].text)

                # 📦 List available resources
                resources = await session.list_resources()
                print("\n📦 Available Resources:")
                for res in resources:
                    print(f" - {res.url}")

                # 📄 Try reading a static resource
                try:
                    static_content = await session.read_resource("resource://some_static_resource")
                    print("\n📄 Static Resource Content:")
                    print(static_content.contents[0].text)
                except Exception as e:
                    print("\n⚠️ Static resource not found or failed to load:", e)

                # 👋 Read dynamic greeting resource
                greeting = await session.read_resource("greeting://yash")
                print("\n👋 Greeting from server:")
                print(greeting.contents[0].text)

                # 💡 List available prompts
                prompts = await session.list_prompts()
                print("\n💡 Available Prompts:")
                for prompt in prompts:
                    print(f" - {prompt.name}")

                # 🧠 Use 'review_code' prompt
                review = await session.get_prompt(
                    "review_code", arguments={"code": 'print("Hello world")'}
                )
                print("\n🧠 Review Code Output:")
                print(review)

                # 🐞 Use 'debug_error' prompt
                debug = await session.get_prompt(
                    "debug_error", arguments={"error": "SyntaxError: invalid syntax"}
                )
                print("\n🐞 Debug Error Output:")
                print(debug)

    except Exception as err:
        print("❌ Failed to connect or communicate with MCP server:", err)


if __name__ == "__main__":
    asyncio.run(run())
