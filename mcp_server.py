
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hello Agent MCP Server")


applications = {
    "HR Portal": {
        "owner": "Human Resources",
        "status": "Active",
        "technology": "Python",
        "vendor": "Microsoft",
        "approval_status": "Approved"
    },
    "Legacy Reports": {
        "owner": "IT Operations",
        "status": "Retirement candidate",
        "technology": "Java",
        "vendor": "Microsoft",
        "approval_status": "Not Approved"
    }
}

@mcp.tool()
def say_hello(name: str) -> str:
    """Return a friendly greeting."""
    return "Hello, " + name + "!"


@mcp.tool()
def get_application(application_name: str) -> dict:
    """Look up an application in the fictional inventory."""
    record = applications.get(application_name)

    if record is None:
        return {
            "found": False,
            "message": "Application not found"
        }

    return {
        "found": True,
        "name": application_name,
        **record
    }

@mcp.tool()
def list_applications() -> dict:
    """List all applications in the fictional inventory."""
    return {
        "count": len(applications),
        "applications": list(applications.keys())
    }
@mcp.tool()
def list_approved_applications_by_vendor(vendor: str) -> dict:
    """List approved applications for a specified vendor."""
    matches = [
        name
        for name, record in applications.items()
        if record.get("vendor", "").casefold() == vendor.strip().casefold()
        and record.get("approval_status", "").casefold() == "approved"
    ]
    return {
        "vendor": vendor,
        "count": len(matches),
        "applications": matches
    }

if __name__ == "__main__":
    mcp.run()
