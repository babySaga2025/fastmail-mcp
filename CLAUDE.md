# Fastmail MCP Server

## Overview
MCP server for managing Fastmail email via JMAP API. Cloned from doronkatz/Fastmail-MCP, extended with custom email management commands.

## Setup
- Python 3.12, virtualenv at `.venv/`
- Install: `.venv/bin/pip install -r requirements.txt`
- Auth: API token in `.env` (`FASTMAIL_TOKEN`), no username/password needed
- Verify connection: `PYTHONPATH=src .venv/bin/python -m fastmail_mcp.cli verify`

## Architecture
- `src/fastmail_mcp/mcp_server.py` — MCP-compliant server (primary entry point)
- `src/fastmail_mcp/server.py` — Legacy JSON-line server (not used)
- `src/fastmail_mcp/client/transport.py` — JMAP protocol layer (HTTP, session, auth)
- `src/fastmail_mcp/client/api.py` — High-level client with fixture fallback
- `src/fastmail_mcp/commands/` — Tool implementations (add new commands here)
- `src/fastmail_mcp/schemas/` — Input validation and response schemas
- `src/fastmail_mcp/models/` — Data structures (Message, Contact, CalendarEvent)

## Adding New Commands
1. Create or edit a file in `commands/` (follow `messages.py` pattern)
2. Register as a `Tool` in `mcp_server.py` with input schema
3. Wire into `call_tool()` in `mcp_server.py`
4. For write operations, gate behind `FASTMAIL_ENABLE_WRITE_TOOLS=true`

## Conventions
- All timestamps displayed in Central Time (America/Chicago) via `utils.format_local()`
- DST handled automatically by stdlib `zoneinfo` — CST in winter, CDT in summer
- Use `format_local()` for any new timestamp output; never hardcode UTC offsets

## What Works
- Mail read operations: list, search, get message details
- Token-based auth (bearer token via FASTMAIL_TOKEN)
- Contacts/calendars exist in code but token is scoped to mail only — not needed

## What Doesn't Work Yet
- `messages-send` is a placeholder (TODO in code)
- No write operations in transport layer (move, archive, delete, set keywords)
- These need JMAP `Email/set` and `Email/submit` methods added to `transport.py`

## Running
```bash
# Verify credentials
PYTHONPATH=src .venv/bin/python -m fastmail_mcp.cli verify

# Run MCP server
PYTHONPATH=src .venv/bin/python -m fastmail_mcp.mcp_server

# Run tests
PYTHONPATH=src .venv/bin/pytest
```

## Code Style
- Black formatter (88 char line limit)
- Ruff linter
- Type hints on public APIs
