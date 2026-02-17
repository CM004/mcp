from typing import Union
from mcp.server.fastmcp import FastMCP
import sqlite3
from pathlib import Path

# Initialize MCP server
mcp = FastMCP("SQLite Database Server")

# Database configuration
DB_FILE = "database.db"

def init_database():
    """Create database and items table"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_FILE}")

# Initialize database on startup
init_database()

# Tool 1: Write Item to Database
@mcp.tool()
def write_item(name: str, description: str = "", value: str = "") -> str:
    """
    Write a new item to the database.
    
    Args:
        name: Name of the item (required)
        description: Description of the item (optional)
        value: Value/price of the item (optional)
    
    Returns:
        Success message with the item ID
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO items (name, description, value) VALUES (?, ?, ?)",
        (name, description, value)
    )
    
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    
    return f"✅ Item added successfully!\nID: {item_id}\nName: {name}"

# Tool 2: Get All Items from Database
@mcp.tool()
def get_items(limit: Union[int,str] = 10) -> str:
    """
    Get all items from the database.
    
    Args:
        limit: Maximum number of items to return (default: 10)

    Returns:
        Formatted list of all items
    """
    limit = int(limit)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM items ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "📭 No items found in database."
    
    result = f"📋 Database Items (Total: {len(rows)}):\n\n"
    
    for row in rows:
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"ID: {row['id']}\n"
        result += f"Name: {row['name']}\n"
        
        if row['description']:
            result += f"Description: {row['description']}\n"
        
        if row['value']:
            result += f"Value: {row['value']}\n"
        
        result += f"Created: {row['created_at']}\n"
    
    result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    return result

# Tool 3: Get Single Item by ID
@mcp.tool()
def get_item_by_id(item_id: int) -> str:
    """
    Get a specific item by its ID.
    
    Args:
        item_id: The ID of the item to retrieve
    
    Returns:
        Item details or error message
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return f"❌ Item with ID {item_id} not found."
    
    result = f"""✅ Item Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: {row['id']}
Name: {row['name']}
Description: {row['description'] or 'N/A'}
Value: {row['value'] or 'N/A'}
Created: {row['created_at']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    return result

# Run server with your preferred transport
if __name__ == "__main__":
    # Change this to: "stdio", "sse", or "streamable-http"
    TRANSPORT = "stdio"
    
    if TRANSPORT == "stdio":
        print("🚀 Starting MCP Server with STDIO transport")
        mcp.run(transport="stdio")
    
    elif TRANSPORT == "sse":
        print("🚀 Starting MCP Server with SSE transport")
        print("📡 Connect at: http://localhost:8000/sse")
        mcp.run(transport="sse")
    
    elif TRANSPORT == "streamable-http":
        print("🚀 Starting MCP Server with Streamable HTTP transport")
        print("📡 Connect at: http://localhost:8000/mcp")
        mcp.run(transport="streamable-http")
