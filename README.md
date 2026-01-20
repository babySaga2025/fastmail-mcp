# Fastmail MCP Server

A Model Context Protocol (MCP) server that provides access to Fastmail email, contacts, and calendar data through a standardized interface.

## Features

- **Email Management**: List, search, and retrieve email messages with advanced filtering
- **Contact Access**: List contacts from your Fastmail address book
- **Calendar Events**: Access calendar events and appointments
- **Date-based Filtering**: Search emails by date ranges
- **Robust Error Handling**: Graceful fallback to sample data when live API is unavailable

## MCP Tools

### Messages
- `messages-list`: List recent email messages with basic filtering
- `messages-search`: Advanced email search with date ranges, sender, subject, and attachment filters
- `messages-get`: Retrieve full details of a specific message

### Contacts
- `contacts-list`: List contacts from address book

### Events
- `events-list`: List calendar events

## Installation & Setup

### 1. Environment Configuration

Create a `.env` file in the project root with your Fastmail credentials:

```bash
FASTMAIL_USERNAME=your.email@fastmail.com
FASTMAIL_APP_PASSWORD=your-app-password
FASTMAIL_BASE_URL=https://api.fastmail.com
FASTMAIL_TOKEN=your-session-token  # Optional: for enhanced authentication
```

**Security Note**: Never commit your `.env` file to version control. Use `.env.example` as a template.

### 2. MCP Client Configuration

To integrate this server with an MCP client (like Claude Desktop, Warp, or other MCP-compatible applications), add the following configuration to your MCP settings file:

```json
{
  "fastmail": {
    "args": [
      "-m",
      "fastmail_mcp.server"
    ],
    "command": "python3",
    "cwd": "/path/to/your/Fastmail-MCP",
    "env": {
      "PYTHONPATH": "/path/to/your/Fastmail-MCP/src"
    }
  }
}
```

**Important**: Replace `/path/to/your/Fastmail-MCP` with the actual absolute path to your Fastmail-MCP directory.

### 3. Fastmail App Password

1. Log in to your Fastmail account
2. Go to Settings > Privacy & Security > App Passwords
3. Create a new app password for this MCP server
4. Use this password in your `.env` file as `FASTMAIL_APP_PASSWORD`

## Development

### Prerequisites

- Python 3.11 or higher
- Required dependencies (install with `pip install -r requirements.txt`)

### Running the Server

For development and testing:

```bash
# Set up Python path and run the server
PYTHONPATH=src python3 -m fastmail_mcp.server
```

### Testing

```bash
# Run the test suite
pytest

# Run with coverage
pytest --cov=fastmail_mcp --cov-report=term-missing

# Verify live connectivity
python3 -m fastmail_mcp.cli verify
```

### Code Quality

```bash
# Lint code
ruff check src tests

# Format code
black src tests
```

## Architecture

```
src/fastmail_mcp/
├── client/           # API clients and transport layer
│   ├── api.py       # High-level Fastmail client
│   └── transport.py # JMAP transport implementation
├── commands/        # MCP command implementations
│   ├── messages.py  # Email-related commands
│   ├── contacts.py  # Contact management commands
│   └── events.py    # Calendar event commands
├── models/          # Data models
├── schemas/         # Request/response schemas
├── server.py        # Legacy MCP server (backwards compatibility)
├── mcp_server.py    # Modern MCP-compliant server
├── cli.py          # Command-line utilities
└── utils.py        # Shared utilities
```

## Usage Examples

Once configured with your MCP client, you can use natural language to interact with your Fastmail data:

- "List my emails from yesterday"
- "Show me unread messages from john@example.com"
- "Find emails with attachments from last week"
- "Get my contacts"
- "Show my calendar events for tomorrow"

## Troubleshooting

### Common Issues

1. **Transport closed error**: Restart your MCP client or check that the server path is correct
2. **Authentication failed**: Verify your app password and username in `.env`
3. **Module not found**: Ensure `PYTHONPATH` is set correctly in your MCP configuration

### Logs and Debugging

The server logs important information to help diagnose issues. When reporting problems, include:
- Your MCP client configuration (without sensitive data)
- Server logs
- The specific command or query that failed

## Security

- **Credentials**: Store all credentials in `.env` file, never in code
- **App Passwords**: Use Fastmail app passwords, not your main account password  
- **Sample Data**: The server includes sample data for testing when live API is unavailable
- **Error Handling**: Graceful degradation to sample data prevents exposure of API errors

## Contributing

1. Follow the coding standards defined in `AGENTS.md`
2. Ensure all tests pass before submitting changes
3. Update documentation for any new features
4. Use conventional commit messages

## License

This project follows the guidelines and structure defined in the repository's agent configuration files.