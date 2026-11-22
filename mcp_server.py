import os
from mcp.server.fastmcp import FastMCP
from inventory_repository import SQLiteInventory, DEFAULT_DB

mcp = FastMCP(
    'Hello Agent MCP Server',
    host=os.environ.get('HELLOAGENT_HOST', '127.0.0.1'),
    port=int(os.environ.get('DATABRICKS_APP_PORT',
                            os.environ.get('HELLOAGENT_PORT', '8000'))),
    streamable_http_path='/mcp',
    stateless_http=True,
    json_response=True,
)
applications = {
    'HR Portal': {'owner': 'Human Resources', 'status': 'Active', 'technology': 'Python', 'vendor': 'Microsoft', 'approval_status': 'Approved'},
    'Legacy Reports': {'owner': 'IT Operations', 'status': 'Retirement candidate', 'technology': 'Java', 'vendor': 'Microsoft', 'approval_status': 'Not Approved'},
}


def repository():
    mode = os.environ.get('HELLOAGENT_BACKEND', 'memory')
    if mode == 'memory':
        return None
    if mode == 'sqlite':
        return SQLiteInventory(os.environ.get('HELLOAGENT_DB', str(DEFAULT_DB)))
    raise ValueError('Unsupported inventory backend')


@mcp.tool()
def say_hello(name: str) -> str:
    """Return a friendly greeting."""
    return 'Hello, ' + name + '!'


@mcp.tool()
def get_application(application_name: str) -> dict:
    """Look up an application in the fictional inventory."""
    db = repository()
    if db is not None:
        return db.get_application(application_name)
    record = applications.get(application_name)
    if record is None:
        return {'found': False, 'message': 'Application not found'}
    return {'found': True, 'name': application_name, **record}


@mcp.tool()
def list_applications() -> dict:
    """List all applications in the fictional inventory."""
    db = repository()
    if db is not None:
        return db.list_applications()
    return {'count': len(applications), 'applications': list(applications)}


@mcp.tool()
def list_approved_applications_by_vendor(vendor: str) -> dict:
    """List approved applications for a specified vendor."""
    db = repository()
    if db is not None:
        return db.list_approved_applications_by_vendor(vendor)
    matches = [name for name, record in applications.items()
               if record.get('vendor', '').casefold() == vendor.strip().casefold()
               and record.get('approval_status', '').casefold() == 'approved']
    return {'vendor': vendor, 'count': len(matches), 'applications': matches}


if __name__ == '__main__':
    mcp.run(transport=os.environ.get(
        'HELLOAGENT_TRANSPORT', 'stdio'))
