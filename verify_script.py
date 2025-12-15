import os
import sys
from dotenv import load_dotenv

# Add current directory to sys.path
sys.path.append(os.getcwd())

# Load env before importing server because server loads env at top level
load_dotenv()

try:
    from src.beancount_fava_mcp.server import get_ledger_data, query_journal, _make_request
except ImportError as e:
    # Try importing via installed package if local import fails
    try:
        from beancount_fava_mcp.server import get_ledger_data, query_journal, _make_request
    except ImportError:
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

    print("\nTesting query_journal tool with new interface...")
    try:
        # Example: account, tag, and payee
        # We need to clean up arguments based on the new signature
        account = "Assets:Balance:Giftcards:Fluz"
        # Assuming user has data matching this, otherwise we receive empty list but success
        payee = "Flu" # Partial match for "Fluz"?
        narration = "Reload" # Partial match for "Opening balance..."
        # Testing the range syntax as requested by user
        time = "2024-12-10 - 2025-W52" 
        
        print(f"Querying: account={account}, payee={payee}, narration={narration}, time={time}")
        data = query_journal(account=account, payee=payee, narration=narration, time=time)
        print(f"query_journal result: {str(data)}...")
    except Exception as e:
        print(f"query_journal failed: {e}")
    except Exception as e:
        print(f"query_journal failed: {e}")

if __name__ == "__main__":
    if test_connection():
        test_tools()
