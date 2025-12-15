import os
import requests
import logging
from typing import Any, List, Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
FAVA_URL = os.getenv("FAVA_URL")
FAVA_USERNAME = os.getenv("FAVA_USERNAME")
FAVA_PASSWORD = os.getenv("FAVA_PASSWORD")

if not FAVA_URL:
    raise ValueError("FAVA_URL environment variable is required")

# Initialize FastMCP server
mcp = FastMCP("beancount-fava")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _make_request(endpoint: str, params: Optional[dict] = None) -> Any:
    """Helper to make authenticated requests to Fava."""
    url = f"{FAVA_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    auth = None
    if FAVA_USERNAME and FAVA_PASSWORD:
        auth = (FAVA_USERNAME, FAVA_PASSWORD)
    
    try:
        response = requests.get(url, auth=auth, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        raise RuntimeError(f"Failed to communicate with Fava: {str(e)}")

@mcp.tool()
def get_ledger_data() -> str:
    """
    List all the data in the ledger including all the full account names, all the tags, all the links.
    """
    try:
        data = _make_request("api/ledger_data")
        # Structure of response needs to be checked, but returning as string for now
        # logic to parse helpful info can be added here
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def query_journal(
    account: str = None, 
    time: str = None,
    tags: list[str] = None,
    links: list[str] = None,
    payee: str = None,
    narration: str = None,
    extra_filter: str = None
) -> str:
    """
    Find user the exact journal entries using specific filters.
    
    Args:
        account: The account to filter by (e.g. 'Assets:Balance')
        time: Time period filter. Supports complex formats:
              - Year: '2015'
              - Quarter: '2012-Q1'
              - Month: '2010-10'
              - Week: '2016-W12'
              - Day: '2015-06-12'
              - Range: '2010 - 2012-10' (inclusive, linked by ' - ')
        tags: List of tags to filter by (e.g. ['vacation', '2024']). logic is AND.
        links: List of links to filter by (e.g. ['invoice-123']). logic is AND.
        payee: Payee name to filter by (supports partial match/regex).
        narration: Narration text to filter by (supports partial match/regex).
        extra_filter: Any additional raw filter string (e.g. 'number > 100').
    """
    params = {
        "query_string": "SELECT *",
    }
    
    # Construct filter list
    filter_parts = []
    
    if account:
        params["account"] = account
        
    if time:
        params["time"] = time
        
    if tags:
        for tag in tags:
            # Ensure tag starts with #
            clean_tag = tag.lstrip('#')
            filter_parts.append(f"#{clean_tag}")
            
    if links:
        for link in links:
            # Ensure link starts with ^
            clean_link = link.lstrip('^')
            filter_parts.append(f"^{clean_link}")
            
    if payee:
        clean_payee = payee.replace('"', '\\"')
        filter_parts.append(f'payee:"{clean_payee}"')
        
    if narration:
        clean_narration = narration.replace('"', '\\"')
        filter_parts.append(f'narration:"{clean_narration}"')
        
    if extra_filter:
        filter_parts.append(extra_filter)
        
    if filter_parts:
        params["filter"] = " ".join(filter_parts)
        
    try:
        data = _make_request("api/query", params=params)
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
