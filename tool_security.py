def validate_tool_name(tool_name):
    """Allow only explicitly authorized MCP tools."""
    allowed_tools = {
        "list_approved_applications_by_vendor",
        "list_applications",
    }

    if tool_name not in allowed_tools:
        raise ValueError("Unsupported MCP tool selection")

    return tool_name

def validate_tool_arguments(tool_name, arguments):
    """Validate arguments before executing an MCP tool."""
    validate_tool_name(tool_name)

    if not isinstance(arguments, dict):
        raise ValueError("Invalid tool arguments")

    if tool_name == "list_applications":
        if arguments != {}:
            raise ValueError("Unexpected arguments for list_applications")

    elif tool_name == "list_approved_applications_by_vendor":
        if set(arguments) != {"vendor"}:
            raise ValueError("Unexpected vendor lookup arguments")

        vendor = arguments["vendor"]
        if not isinstance(vendor, str) or not vendor.strip():
            raise ValueError("Invalid vendor")

    return arguments
