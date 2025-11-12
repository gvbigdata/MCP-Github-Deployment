import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# In-memory task storage
tasks = {}
task_counter = 0

# Create server
server = Server("task-manager")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="add_task",
            description="Add a new task to the task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional)"
                    }
                },
                "required": ["title"]
            }
        ),
        types.Tool(
            name="list_tasks",
            description="List all tasks",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "number",
                        "description": "ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        ),
        types.Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "number",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution."""
    global task_counter
    
    if name == "add_task":
        task_counter += 1
        title = arguments.get("title", "")
        description = arguments.get("description", "")
        
        tasks[task_counter] = {
            "id": task_counter,
            "title": title,
            "description": description,
            "completed": False
        }
        
        return [
            types.TextContent(
                type="text",
                text=f"✅ Task added successfully!\nID: {task_counter}\nTitle: {title}"
            )
        ]
    
    elif name == "list_tasks":
        if not tasks:
            return [
                types.TextContent(
                    type="text",
                    text="No tasks found. Add a task to get started!"
                )
            ]
        
        task_list = "📋 Task List:\n\n"
        for task_id, task in tasks.items():
            status = "✓" if task["completed"] else "○"
            task_list += f"{status} [{task_id}] {task['title']}\n"
            if task["description"]:
                task_list += f"   └─ {task['description']}\n"
        
        return [
            types.TextContent(
                type="text",
                text=task_list
            )
        ]
    
    elif name == "complete_task":
        task_id = int(arguments.get("task_id", 0))
        
        if task_id not in tasks:
            return [
                types.TextContent(
                    type="text",
                    text=f"❌ Task {task_id} not found"
                )
            ]
        
        tasks[task_id]["completed"] = True
        return [
            types.TextContent(
                type="text",
                text=f"✅ Task {task_id} marked as completed: {tasks[task_id]['title']}"
            )
        ]
    
    elif name == "delete_task":
        task_id = int(arguments.get("task_id", 0))
        
        if task_id not in tasks:
            return [
                types.TextContent(
                    type="text",
                    text=f"❌ Task {task_id} not found"
                )
            ]
        
        deleted_task = tasks.pop(task_id)
        return [
            types.TextContent(
                type="text",
                text=f"🗑️ Task deleted: {deleted_task['title']}"
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the server using stdin/stdout streams."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="task-manager",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

def run_server():
    """Entry point for the server."""
    import asyncio
    asyncio.run(main())

if __name__ == "__main__":
    run_server()