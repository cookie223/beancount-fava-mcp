import os
import sys
from dotenv import load_dotenv

# Add current directory to sys.path
sys.path.append(os.getcwd())

# Load env before importing server because server loads env at top level
load_dotenv()

try:
    from server import get_ledger_data, query_journal, _make_request
except ImportError as e:
    print(f"Failed to import server: {e}")
    sys.exit(1)

def test_connection():
    print("Testing connection to Fava...")
    try:
        # Try a simple fetch manually first to debug if needed
        data = _make_request("api/ledger_data")
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def test_tools():
    print("\nTesting get_ledger_data tool...")
    try:
        data = get_ledger_data()
        print(f"get_ledger_data result (truncated): {str(data)[:200]}...")
    except Exception as e:
        print(f"get_ledger_data failed: {e}")

    print("\nTesting query_journal tool...")
    try:
        # Using the example from the prompt
        account = "Assets:Balance:Giftcards:Fluz"
        filter_str = 'payee:"Fluz"'
        time = "2025-12-15"
        data = query_journal(account=account, filter_str=filter_str, time=time)
        print(f"query_journal result: {str(data)}")
    except Exception as e:
        print(f"query_journal failed: {e}")

if __name__ == "__main__":
    if test_connection():
        test_tools()
