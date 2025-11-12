# Task MCP Server

A simple task management Model Context Protocol (MCP) server for Claude Desktop.

## Features

- ✅ Add new tasks
- 📋 List all tasks
- ✓ Mark tasks as completed
- 🗑️ Delete tasks

## Installation

### From GitHub (Recommended)

The easiest way to use this server is directly from GitHub using `uvx`:

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "uvx",
      "args": [
        "task-mcp-server",
        "--from",
        "git+https://github.com/YOUR_USERNAME/task-mcp-server.git"
      ]
    }
  }
}
```

### Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/task-mcp-server.git
cd task-mcp-server

# Install with uv
uv pip install -e .

# Run the server
task-mcp-server
```

## Usage with Claude Desktop

1. Open Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "uvx",
      "args": [
        "task-mcp-server",
        "--from",
        "git+https://github.com/YOUR_USERNAME/task-mcp-server.git"
      ]
    }
  }
}
```

3. Restart Claude Desktop

4. Look for the 🔌 icon to confirm the server is connected

## Available Tools

- **add_task**: Add a new task with title and optional description
- **list_tasks**: Display all tasks with their status
- **complete_task**: Mark a task as completed
- **delete_task**: Remove a task from the list

## Example Usage

In Claude Desktop, try:
- "Add a task to buy groceries"
- "List all my tasks"
- "Mark task 1 as completed"
- "Delete task 2"

## Development

```bash
# Install dependencies
uv pip install -e .

# Run locally
uv run task-mcp-server

# Test with MCP inspector
npx @modelcontextprotocol/inspector uv run task-mcp-server
```

## License

MIT