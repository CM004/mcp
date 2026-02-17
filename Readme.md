**Manual Tool Mapping** for the SQLite database MCP server.

### Why I Used It:

1. **Full Control Over Tool Behavior**
   - We manually created 3 specific tools (`write_item`, `get_items`, `get_item_by_id`) with custom formatting and business logic. This allowed us to format database responses in structure, making it easy for AI agents to understand and present to users.

2. **No External API Dependency**
   - We built the MCP server directly on SQLite database operations, not wrapping existing REST APIs. Manual mapping was necessary because there was no OpenAPI spec to auto-convert from - we defined the tools from scratch.

3. **Learning**
   - Manual approach helped understand MCP fundamentals: how tools work, parameter handling, and response formatting. This hands-on experience be used in automated approaches in production.

### When to Use This in Production:

**Use Manual Mapping in production when:**
-  You need **security control** - selectively expose only safe operations to AI
-  You need **custom business logic** - validate, transform, or aggregate data before returning to AI
-  You need **optimized AI responses** - format output specifically for LLM reasoning (like our formatted item lists with emojis and structure)

**Perfect for:** Internal tools, admin dashboards, or sensitive business operations where you want precise control over what AI can do.