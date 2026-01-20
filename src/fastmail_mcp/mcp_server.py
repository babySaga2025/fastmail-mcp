"""MCP-compliant server implementation for Fastmail."""

import asyncio
import os
from pathlib import Path
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, ServerCapabilities, ToolsCapability

from fastmail_mcp.client import FastmailClient
from fastmail_mcp.commands.messages import list_messages, get_message, search_messages
from fastmail_mcp.commands.contacts import list_contacts
from fastmail_mcp.commands.events import list_events
from fastmail_mcp.utils import load_env


def build_client() -> FastmailClient:
    """Build Fastmail client with environment configuration."""
    # Load .env from the project root directory, not the current working directory
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / ".env"
    load_env(env_file if env_file.exists() else None)

    base_url = os.environ.get("FASTMAIL_BASE_URL", "https://api.fastmail.com")
    username = os.environ.get("FASTMAIL_USERNAME", "local-user")
    app_password = os.environ.get("FASTMAIL_APP_PASSWORD", "local-app-password")
    token = os.environ.get("FASTMAIL_TOKEN")

    return FastmailClient(
        base_url=base_url,
        username=username,
        app_password=app_password,
        token=token or None,
    )


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("fastmail-mcp")
    client = build_client()

    # Define available tools
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="messages-list",
                description="List email messages with optional filtering",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID"},
                        "mailbox_name": {
                            "type": "string",
                            "description": "Mailbox name (default: INBOX)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of messages to return",
                        },
                        "has_attachment": {
                            "type": "boolean",
                            "description": "Filter messages with attachments",
                        },
                    },
                },
            ),
            Tool(
                name="messages-search",
                description="Search email messages with advanced filtering including date ranges",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID"},
                        "sender": {
                            "type": "string",
                            "description": "Filter by sender email",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Filter by subject text",
                        },
                        "mailbox": {
                            "type": "string",
                            "description": "Filter by mailbox name",
                        },
                        "read": {
                            "type": "boolean",
                            "description": "Filter by read status",
                        },
                        "has_attachment": {
                            "type": "boolean",
                            "description": "Filter messages with attachments",
                        },
                        "date_start": {
                            "type": "string",
                            "description": "Start date (YYYY-MM-DD format)",
                        },
                        "date_end": {
                            "type": "string",
                            "description": "End date (YYYY-MM-DD format)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of messages to return",
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Number of messages to skip",
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "Sort field (receivedAt, sentAt, subject)",
                        },
                        "sort_ascending": {
                            "type": "boolean",
                            "description": "Sort in ascending order",
                        },
                    },
                },
            ),
            Tool(
                name="messages-get",
                description="Get full details of a specific message",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID"},
                        "message_id": {
                            "type": "string",
                            "description": "Message ID",
                            "required": True,
                        },
                    },
                    "required": ["message_id"],
                },
            ),
            Tool(
                name="contacts-list",
                description="List contacts from address book",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID"},
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of contacts to return",
                        },
                    },
                },
            ),
            Tool(
                name="events-list",
                description="List calendar events",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID"},
                        "calendar_name": {
                            "type": "string",
                            "description": "Calendar name",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of events to return",
                        },
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[Any]:
        """Handle tool calls."""
        if name == "messages-list":
            # Convert limit to int if present
            if "limit" in arguments:
                arguments["limit"] = int(arguments["limit"])
            result = list_messages(client=client, **arguments)
            return [{"type": "text", "text": str(result)}]
        elif name == "messages-search":
            # Convert numeric arguments to proper types
            if "limit" in arguments:
                arguments["limit"] = int(arguments["limit"])
            if "offset" in arguments:
                arguments["offset"] = int(arguments["offset"])
            result = search_messages(client=client, **arguments)
            return [{"type": "text", "text": str(result)}]
        elif name == "messages-get":
            result = get_message(client=client, **arguments)
            return [{"type": "text", "text": str(result)}]
        elif name == "contacts-list":
            # Convert limit to int if present
            if "limit" in arguments:
                arguments["limit"] = int(arguments["limit"])
            result = list_contacts(client=client, **arguments)
            return [{"type": "text", "text": str(result)}]
        elif name == "events-list":
            # Convert limit to int if present
            if "limit" in arguments:
                arguments["limit"] = int(arguments["limit"])
            result = list_events(client=client, **arguments)
            return [{"type": "text", "text": str(result)}]
        else:
            raise ValueError(f"Unknown tool: {name}")

    return server


async def main():
    """Main entry point for the MCP server."""
    server = create_server()

    # Run the server using stdio transport
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="fastmail-mcp",
                server_version="0.1.0",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability(listChanged=False)
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
