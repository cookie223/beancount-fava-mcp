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
def query_journal(account: Optional[str] = None, filter_str: Optional[str] = None, time: Optional[str] = None) -> str:
    """
    Find user the exact journal entries.
    
    Args:
        account: The account to filter by (e.g. 'Assets:Balance:Giftcards:Fluz')
        filter_str: Beancount query filter string (e.g. '#11IGF5GLD payee:"Fluz"')
        time: Time period filter (e.g. '2024 - day')
    """
    # Use api/query with SELECT * to get entries in JSON format.
    # Fava's api/query endpoint respects 'account', 'filter', and 'time' params
    # to contextually filter the data before running the query.
    params = {
        "query_string": "SELECT *",
    }
    if account:
        params["account"] = account
    if filter_str:
        params["filter"] = filter_str
    if time:
        params["time"] = time
        
    try:
        data = _make_request("api/query", params=params)
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
