import argparse
import os
import sys

# We need to set env vars before importing server if server had global logic, 
# but we refactored server.py to read env vars inside _make_request.
# However, importing argparse and running logic usually happens in main block.

def main():
    parser = argparse.ArgumentParser(description="Beancount Fava MCP Server")
    parser.add_argument("--fava-url", help="URL of the Fava instance")
    parser.add_argument("--username", help="Fava username")
    parser.add_argument("--password", help="Fava password")
    
    # Parse known args, leaving the rest for mcp if needed, 
    # BUT mcp libraries usually grab sys.argv.
    # We should consume our args and leave sys.argv clean or 
    # manually invoke mcp.run().
    
    args, unknown = parser.parse_known_args()
    
    if args.fava_url:
        os.environ["FAVA_URL"] = args.fava_url
    if args.username:
        os.environ["FAVA_USERNAME"] = args.username
    if args.password:
        os.environ["FAVA_PASSWORD"] = args.password
        
    # Remove our arguments from sys.argv so mcp doesn't choke on them if it parses args
    # FastMCP uses typer/click usually?
    # If we call mcp.run(), it might look at argv.
    sys.argv = [sys.argv[0]] + unknown
    
    from .server import mcp
    mcp.run()

if __name__ == "__main__":
    main()
