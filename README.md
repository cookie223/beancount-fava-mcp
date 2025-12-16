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

- Get ledger data
- Get accounts
- Get currencies
- Get payees
- Get tags
- Get links
- Query journal
- Run BQL

## Future Plans

- Support some kind of write access to the ledger so that you can add transactions easily via your mcp client.

## Usage

Can be used with Claude Desktop or other MCP clients.
