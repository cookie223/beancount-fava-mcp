
import logging
from unittest.mock import MagicMock, patch
from beancount_fava_mcp.server import add_entry

# Mock requests.put
@patch('beancount_fava_mcp.server.requests.put')
@patch('beancount_fava_mcp.server._get_config')
def test_add_entry(mock_get_config, mock_put):
    # Setup mocks
    mock_get_config.return_value = ("http://localhost:5000", "user", "pass")
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status.return_value = None
    mock_put.return_value = mock_response

    # Test data
    date = "2025-12-16"
    payee = "Test Payee"
    narration = "Test Narration"
    postings = [
        {"account": "Expenses:Test", "amount": "10.00 USD"},
        {"account": "Assets:Test", "amount": "-10.00 USD"}
    ]
    
    # Call the tool
    result = add_entry(date=date, payee=payee, narration=narration, postings=postings)
    
    # Verify calls
    print(f"Result: {result}")
    
    # Verify arguments passed to put
    args, kwargs = mock_put.call_args
    print(f"URL called: {args[0]}")
    print(f"JSON payload: {kwargs['json']}")
    
    expected_payload = {
        "entries": [{
            "t": "Transaction",
            "date": date,
            "payee": payee,
            "narration": narration,
            "postings": postings,
            "tags": [],
            "links": [],
            "meta": {}
        }]
    }
    
    assert kwargs['json'] == expected_payload
    print("Payload verification passed!")

if __name__ == "__main__":
    test_add_entry()
