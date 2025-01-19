import pytest
from unittest.mock import patch

from modules.host_info import get_host_name


# Positive Test: Valid host name
@patch("socket.gethostname")
def test_get_host_name_valid(mock_gethostname):
    mock_gethostname.return_value = "test-host"
    
    result = get_host_name()
    assert result == "Host Name: test-host"

# Test: Simulating empty host name (edge case)
@patch("socket.gethostname")
def test_get_host_name_empty(mock_gethostname):
    mock_gethostname.return_value = ""
    
    result = get_host_name()
    assert result == "Host Name: "

# Test: Simulating a long host name (edge case)
@patch("socket.gethostname")
def test_get_host_name_long(mock_gethostname):
    mock_gethostname.return_value = "a" * 256
    
    result = get_host_name()
    assert result == f"Host Name: {'a' * 256}"
