# Create a new directory for our project
uv init folder name
cd folder name

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx
