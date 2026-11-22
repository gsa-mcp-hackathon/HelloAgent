"""HelloAgent stdio client with explicit inventory backend configuration."""
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _call_tool(tool, arguments):
    server_file = Path(__file__).with_name('mcp_server.py')
    env = {'HELLOAGENT_BACKEND': os.environ.get('HELLOAGENT_BACKEND', 'memory')}
    if 'HELLOAGENT_DB' in os.environ:
        env['HELLOAGENT_DB'] = os.environ['HELLOAGENT_DB']
    server = StdioServerParameters(command=sys.executable, args=[str(server_file)], env=env)
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, arguments=arguments)
            if result.isError:
                raise RuntimeError(f'MCP tool failed: {tool}')
            for item in result.content:
                if item.type == 'text':
                    return item.text
            raise RuntimeError(f'No text response from MCP tool: {tool}')


async def get_greeting(name):
    return await _call_tool('say_hello', {'name': name})


async def get_application_details(application_name):
    return await _call_tool('get_application', {'application_name': application_name})


async def get_application_list():
    return await _call_tool('list_applications', {})


async def get_approved_applications_by_vendor(vendor):
    return await _call_tool('list_approved_applications_by_vendor', {'vendor': vendor})
