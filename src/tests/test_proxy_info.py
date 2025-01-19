import pytest
import os
from unittest.mock import patch

from modules.proxy_info import get_proxy_info

# Positive Test: Proxy with both IP and Port
@patch.dict(os.environ, {'http_proxy': 'http://192.168.1.1:8080'})
def test_get_proxy_info_with_proxy():
    result = get_proxy_info()
    assert result == "Proxy enabled: IP = 192.168.1.1, Port = 8080"

# Positive Test: Proxy with IP and no Port
@patch.dict(os.environ, {'http_proxy': 'http://192.168.1.1'})
def test_get_proxy_info_with_no_port():
    result = get_proxy_info()
    assert result == "Proxy enabled: IP = 192.168.1.1, Port = Not specified"

# Negative Test: No proxy configured
@patch.dict(os.environ, {})
def test_get_proxy_info_no_proxy():
    result = get_proxy_info()
    assert result == "No proxy configured."

# Test when both http_proxy and https_proxy are set
@patch.dict(os.environ, {'http_proxy': 'http://192.168.1.1:8080', 'https_proxy': 'https://192.168.1.2:9090'})
def test_get_proxy_info_both_http_and_https():
    result = get_proxy_info()
    assert result == "Proxy enabled: IP = 192.168.1.1, Port = 8080"  # It should take the first available proxy

# Test for the `https_proxy` environment variable
@patch.dict(os.environ, {'https_proxy': 'https://192.168.1.2:9090'})
def test_get_proxy_info_https_proxy():
    result = get_proxy_info()
    assert result == "Proxy enabled: IP = 192.168.1.2, Port = 9090"
