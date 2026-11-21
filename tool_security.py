def validate_tool_name(tool_name):
    """Allow only explicitly authorized MCP tools."""
    allowed_tools = {
        "list_approved_applications_by_vendor",
        "list_applications",
    }

    if tool_name not in allowed_tools:
        raise ValueError("Unsupported MCP tool selection")

    return tool_name