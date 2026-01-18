# Testing Strategy and Mock Harness Plan (Mail-only)

## Purpose

Define the testing approach for the Fastmail MCP server, covering unit tests,
mocked JMAP flows, and minimal integration coverage. Contacts and calendar
remain out of scope until Fastmail exposes JMAP tokens for them.

## Scope

In:
- Unit test strategy for JMAP client, mappers, schemas, and mail tools.
- Mock harness strategy for JMAP responses and offline validation.
- Minimal integration tests for end-to-end tool calls over stdio.

Out:
- Contacts/calendar fixtures until JMAP tokens are available.
- Load/performance testing (documented only if needed later).

## Test Plan

### Unit tests (primary)

Coverage focus:
- JMAP transport request building, response parsing, and error mapping.
- Mail schema validation, mapping, and sorting logic.
- Command handlers (messages list, mailbox listing) with stub transports.

Coverage targets:
- New or modified modules should reach >= 85% coverage.
- CI enforces >= 80% overall coverage via pytest flags.

### Mock harness tests (offline JMAP)

Goal: validate mail flows without real accounts or live network access.

Approach:
- Keep a "transport-injection" path for unit tests (as in `DummyTransport`).
- Add a lightweight JMAP stub server for request/response validation using the
  Python stdlib (`http.server`) or a minimal pytest fixture that intercepts
  `requests` in the transport layer.
- Store request/response pairs as JSON fixtures under `tests/fixtures/jmap/`.
- Ensure fixtures are sanitized and contain no real PII or secrets.

### Integration tests (MCP server)

Minimal end-to-end assertions:
- `FastmailMCPServer` handles known commands and returns structured output.
- Round-trip a `messages-list` request through the server with a stub client.
- Validate error responses for unknown commands and malformed payloads.

### Live tests (opt-in)

- Guard with `FASTMAIL_LIVE_TESTS=1` and `@pytest.mark.slow`.
- Use real credentials only on developer machines.
- Never run in CI by default.

## Mock Harness Design

### Fixture layout

Proposed fixture directory:
- `tests/fixtures/jmap/`

Fixture naming convention:
- `{method}_{scenario}.json` (example: `email_query_success.json`)

Fixture schema:
- Store both request and response in a single object:
  ```json
  {
    "request": { "methodCalls": [...] },
    "response": { "methodResponses": [...] }
  }
  ```

### Harness behavior

- The stub server reads the fixture, matches on method name + arguments, and
  returns the canned response.
- Include deterministic error responses to validate error handling paths.
- Enable an "assert-only" mode that verifies outgoing payloads without making
  assertions on the response body.

## Fixture List (Mail)

Minimum set of fixtures to cover common flows:
- `email_query_success.json`
- `email_get_success.json`
- `email_get_missing_preview.json`
- `email_query_empty.json`
- `email_query_paginated.json`
- `mailbox_get_success.json`
- `mailbox_get_with_roles.json`
- `email_changes_incremental.json`
- `email_changes_has_more.json`
- `error_invalid_auth.json`
- `error_rate_limited.json`
- `error_invalid_arguments.json`

## Error and Edge Cases

Explicitly cover:
- Network timeouts and transport errors.
- Auth failures (401/403) and invalid credentials.
- Missing optional capabilities in session discovery.
- JMAP error responses with `notFound` or partial results.
- Empty mailbox or no messages returned.
- Pagination edges (limit 0, max limit, position offsets).
- Messages missing optional fields (preview, subject, attachments).
- Out-of-order results and duplicate IDs in responses.

## CI-Friendly Test Commands

Recommended CI steps:
- `ruff check src tests`
- `black --check src tests`
- `python3 -m pytest tests/ --cov=fastmail_mcp --cov-report=term-missing --cov-fail-under=80`
- `PYTHONPATH=src python3 -m fastmail_mcp.server --help`

Optional (local only):
- `FASTMAIL_LIVE_TESTS=1 python3 -m pytest tests/integration/ -m slow`

## Open Questions

- Do we want the mock harness to assert payload ordering for method calls?
- Should fixture coverage include mailbox permissions and rights edge cases?
- Do we want a dedicated fixture for corrupted JSON payloads?
