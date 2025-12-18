import os
import requests
import logging
from typing import Any, List, Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("beancount-fava")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_config():
    url = os.getenv("FAVA_URL")
    username = os.getenv("FAVA_USERNAME")
    password = os.getenv("FAVA_PASSWORD")
    if not url:
        raise ValueError("FAVA_URL environment variable is required")
    return url, username, password

def _make_request(endpoint: str, params: Optional[dict] = None, method: str = "GET", json_data: Optional[dict] = None) -> Any:
    """Helper to make authenticated requests to Fava."""
    url, username, password = _get_config()
    
    full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    auth = None
    if username and password:
        auth = (username, password)
    
    try:
        if method == "GET":
            response = requests.get(full_url, auth=auth, params=params)
        elif method == "PUT":
            response = requests.put(full_url, auth=auth, params=params, json=json_data)
        else:
             raise ValueError(f"Unsupported method: {method}")
            
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {full_url}: {e}")
        raise RuntimeError(f"Failed to communicate with Fava: {str(e)}")

@mcp.tool()
def get_ledger_data() -> str:
    """
    List all the data in the ledger including all the full account names, all the tags, all the links.
    """
    try:
        data = _make_request("api/ledger_data")
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_accounts() -> str:
    """
    Get the list of all accounts in the ledger.
    """
    try:
        data = _make_request("api/ledger_data")
        if isinstance(data, dict) and "accounts" in data:
            return str(data["accounts"])
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_currencies() -> str:
    """
    Get the list of all currencies/commodities in the ledger.
    """
    try:
        data = _make_request("api/ledger_data")
        if isinstance(data, dict) and "commodities" in data:
            return str(data["commodities"])
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_payees() -> str:
    """
    Get the list of all payees in the ledger.
    """
    try:
        data = _make_request("api/ledger_data")
        if isinstance(data, dict) and "payees" in data:
            return str(data["payees"])
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_tags() -> str:
    """
    Get the list of all tags in the ledger.
    """
    try:
        data = _make_request("api/ledger_data")
        if isinstance(data, dict) and "tags" in data:
            return str(data["tags"])
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_links() -> str:
    """
    Get the list of all links in the ledger.
    """
    try:
        data = _make_request("api/ledger_data")
        if isinstance(data, dict) and "links" in data:
            return str(data["links"])
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

@mcp.tool()
def run_bql(query: str) -> str:
    """
    Execute a raw Beancount Query Language (BQL) query.
    
    Args:
        query: The BQL query string to execute.
    """
    try:
        params = {"query_string": query}
        data = _make_request("api/query", params=params)
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def add_transaction(
    date: str,
    payee: str,
    narration: str,
    postings: List[dict],
    tags: Optional[List[str]] = None,
    links: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
    flag: Optional[str] = "*"
) -> str:
    """
    Add a new entry (Transaction) to the ledger.
    
    IMPORTANT: ASK THE USER TO REVIEW THE TRANSACTION DETAILS BEFORE CALLING THIS TOOL.
    
    Args:
        date: The date of the transaction (YYYY-MM-DD).
        payee: The payee string.
        narration: The narration string.
        postings: A list of postings. Each posting is a dict with:
                  - 'account': str (e.g. 'Expenses:Food')
                  - 'amount': str (e.g. '10.00 USD') - The full amount string including currency.
                               For complex postings (prices, costs), put the full string here 
                               (e.g. '10 AAPL {150 USD} @ 160 USD').
        tags: Optional list of tags.
        links: Optional list of links.
        metadata: Optional dictionary of metadata.
        flag: Flag for the transaction. Defaults to "*" means posted or cleared, it can be "!" to mean needs attention
    """
    try:
        # Validate accounts
        ledger_data = _make_request("api/ledger_data")
        # Ensure we have a set of stripped strings
        valid_accounts = {str(a).strip() for a in ledger_data.get("accounts", [])}
        
        for p in postings:
            raw_account = p.get("account", "")
            account = str(raw_account).strip()
            
            # Update the posting with the clean account name
            p["account"] = account
            
            if account not in valid_accounts:
                return f"Error: Account '{account}' does not exist in the ledger. Please check the account name or create it first. Available accounts count: {len(valid_accounts)}"

        entry = {
            "t": "Transaction",
            "flag": flag,
            "date": date,
            "payee": payee,
            "narration": narration,
            "postings": postings,
            "tags": tags or [],
            "links": links or [],
            "meta": metadata or {}
        }
        
        # Fava expects a list of entries
        payload = {"entries": [entry]}
        
        data = _make_request("api/add_entries", method="PUT", json_data=payload)
        return f"Success: {str(data)}"
    except Exception as e:
        return f"Error adding entry: {str(e)}"
