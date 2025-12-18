
import logging
from unittest.mock import MagicMock, patch
from beancount_fava_mcp.server import add_transaction

@patch('beancount_fava_mcp.server.requests.get')
@patch('beancount_fava_mcp.server.requests.put')
@patch('beancount_fava_mcp.server._get_config')
def test_nested_validation(mock_get_config, mock_put, mock_get):
    # Setup mocks
    mock_get_config.return_value = ("http://localhost:5000", "user", "pass")
    
    # Mock ledger data response with nested structure (Real Fava behavior)
    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {
        "data": {
            "accounts": ["Assets:Cash", "Expenses:Food"]
        },
        "mtime": 12345
    }
    mock_get_response.raise_for_status.return_value = None
    mock_get.return_value = mock_get_response

    mock_put_response = MagicMock()
    mock_put_response.json.return_value = {"success": True}
    mock_put.return_value = mock_put_response

    # Test 1: Valid
    print("Test 1: Valid Account with Nested Response")
    result_valid = add_transaction(
        date="2025-12-16",
        payee="Test",
        narration="Valid Nested",
        postings=[
            {"account": "Assets:Cash", "amount": "-10 USD"},
            {"account": "Expenses:Food", "amount": "10 USD"}
        ]
    )
    print(f"Result (Valid): {result_valid}")
    assert "Success" in result_valid
    
    print("Nested Validation Verification Passed!")

if __name__ == "__main__":
    test_nested_validation()
