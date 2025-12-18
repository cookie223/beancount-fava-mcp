# Beancount Fava MCP Server

An MCP server to interface with Beancount Fava.

## Installation

```bash
uvx beancount-fava-mcp@latest --fava-url=https://your-fava-instance/ledger-name
```

This is a beancount MCP that relies on a fava instance to provide the data instead of reading the beancount files directly. So this is allowed to be installed on a completely different machine than where your beancount files are stored.

It allows for simple authentication, but it is optional. You can set the following environment variables:

- `FAVA_URL`: The URL of your Fava instance (overrides the --fava-url argument)
- `FAVA_USERNAME`: The username to authenticate with
- `FAVA_PASSWORD`: The password to authenticate with

## Features

- `get_ledger_data()`: List all ledger data including account names, tags, and links.
- `get_accounts()`: Get the list of all accounts.
- `get_currencies()`: Get the list of all currencies/commodities.
- `get_payees()`: Get the list of all payees.
- `get_tags()`: Get the list of all tags.
- `get_links()`: Get the list of all links.
- `query_journal(account, time, tags, links, payee, narration, extra_filter)`: Filter journal entries.
- `run_bql(query)`: Execute raw Beancount Query Language queries.
- `add_transaction(date, payee, narration, postings, tags, links, metadata, flag)`: Add a new transaction entry. **Note:** Review the transaction details carefully before execution.

## Future Plans

- Support some kind of write access to the ledger so that you can add transactions easily via your mcp client. (add_transaction added but still WIP)

## Usage

Can be used with Claude Desktop or other MCP clients.
