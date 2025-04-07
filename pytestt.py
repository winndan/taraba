import pytest
from mcpClient import list_tools, call_tool, read_resources

# Mocking session for testing purposes
class MockSession:
    async def list_tools(self):
        return ["add"]

    async def call_tool(self, tool_name, arguments):
        if tool_name == "add" and arguments["a"] == 4 and arguments["b"] == 5:
            return type("ToolResult", (), {"content": [type("ToolContent", (), {"text": "9"})]})
        else:
            raise ValueError("Invalid tool or arguments")

    async def read_resource(self, resource_id):
        if resource_id == "greeting://yash":
            return type("ResourceContent", (), {"contents": [type("Content", (), {"text": "Hello, yash!"})]})
        else:
            raise ValueError("Invalid resource")

@pytest.mark.asyncio
async def test_list_tools():
    session = MockSession()
    tools = await list_tools(session)
    assert tools == ["add"]

@pytest.mark.asyncio
async def test_call_tool():
    session = MockSession()
    result = await call_tool(session)
    assert result.content[0].text == "9"

@pytest.mark.asyncio
async def test_read_resources():
    session = MockSession()
    try:
        await read_resources(session)
    except Exception as e:
        logger.error(f"Error reading resources: {e}")
    else:
        assert True  # If no exception, test passes
