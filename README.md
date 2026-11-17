# HelloAgent - MCP Software Approval Lookup

## Overview

HelloAgent is a Python MCP demonstration developed for the
GSA MCP Hackathon.

It answers questions about a fictional enterprise software
inventory, including:

"Which applications from Microsoft are approved for use?"

## Architecture

- app.py: Streamlit chat interface
- mcp_client.py: MCP client using stdio transport
- mcp_server.py: MCP server and fictional inventory
- test_helloagent.py: Automated filtering tests

The interface uses keyword-based routing to invoke MCP tools.
It does not currently use an LLM or autonomous agent planning.

## Requirements

Tested locally on Windows with Python 3.14.

Install dependencies:

    python -m pip install -r requirements.txt

## Run the Application

    python -m streamlit run app.py

Open the local URL displayed by Streamlit.

## Example Queries

- Which applications from Microsoft are approved for use?
- list
- lookup HR Portal

## MCP Tools

- say_hello
- get_application
- list_applications
- list_approved_applications_by_vendor

## Testing

Run:

    python test_helloagent.py

Verified local results:

- Five automated tests passed.
- Microsoft approval query succeeded through MCP.
- Five consecutive MCP calls returned expected identical results.
- Streamlit browser demonstration succeeded.

These tests do not establish production reliability.

## Security and Limitations

- Inventory records are fictional.
- No real agency approval data is used.
- No user authentication or role-based authorization is implemented.
- Approval-status filtering is not user authorization.
- The inventory is stored in memory.
- The interface uses keyword-based routing, not an LLM.
- Clean-environment portability has not yet been verified.
- The application is intended for demonstration, not production.

## Project Status

Core MCP functionality and the Streamlit demonstration have
been verified locally. Evaluation documentation and presentation
materials are being prepared for the GSA MCP Hackathon.
