
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def get_greeting(name):
    server_file = Path(__file__).with_name("mcp_server.py")

    server = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "say_hello",
                arguments={"name": name},
            )

            if result.isError:
                raise RuntimeError("MCP tool returned an error")

            for item in result.content:
                if item.type == "text":
                    return item.text

            raise RuntimeError("No text response from MCP tool")

async def get_application_details(application_name):
    server_file = Path(__file__).with_name("mcp_server.py")

    server = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_application",
                arguments={"application_name": application_name},
            )

            if result.isError:
                raise RuntimeError("Inventory lookup failed")

            for item in result.content:
                if item.type == "text":
                    return item.text

            raise RuntimeError("No inventory data returned")

async def get_application_list():
    server_file = Path(__file__).with_name("mcp_server.py")

    server = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "list_applications",
                arguments={},
            )

            if result.isError:
                raise RuntimeError("Application list failed")

            for item in result.content:
                if item.type == "text":
                    return item.text

            raise RuntimeError("No application list returned")


async def get_approved_applications_by_vendor(vendor):
    server_file = Path(__file__).with_name("mcp_server.py")

    server = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "list_approved_applications_by_vendor",
                arguments={"vendor": vendor},
            )

            if result.isError:
                raise RuntimeError("Approved application lookup failed")

            for item in result.content:
                if item.type == "text":
                    return item.text

            raise RuntimeError("No approved application data returned")
