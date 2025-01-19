import pytest
import socket
from unittest.mock import patch, MagicMock

from modules.network_info import get_ipv4_info

# Positive Test: Linux, Static IP (file found and contains IP)
@patch("platform.system", return_value="Linux")
@patch("psutil.net_if_addrs")
@patch("builtins.open", create=True)
def test_ipv4_info_linux_static_ip(mock_open, mock_net_if_addrs, mock_system):
    mock_net_if_addrs.return_value = {
        "eth0": [MagicMock(family=socket.AF_INET, address="192.168.1.100", netmask="255.255.255.0")]
    }
    mock_open.return_value.__enter__.return_value.read.return_value = "192.168.1.100"
    result = get_ipv4_info()
    assert result == "Interface: eth0, IP: 192.168.1.100, Type: Static, Connection: Ethernet"


# Positive Test: Linux, Dynamic IP (file found but does not contain IP)
@patch("platform.system", return_value="Linux")
@patch("psutil.net_if_addrs")
@patch("builtins.open", create=True)
def test_ipv4_info_linux_dynamic_ip(mock_open, mock_net_if_addrs, mock_system):
    mock_net_if_addrs.return_value = {
        "wlan0": [MagicMock(family=socket.AF_INET, address="192.168.1.101", netmask="255.255.255.0")]
    }
    mock_open.return_value.__enter__.return_value.read.return_value = ""
    result = get_ipv4_info()
    assert result == "Interface: wlan0, IP: 192.168.1.101, Type: Dynamic, Connection: Wi-Fi"


# Positive Test: Windows, Dynamic IP
@patch("platform.system", return_value="Windows")
@patch("psutil.net_if_addrs")
def test_ipv4_info_windows_dynamic_ip(mock_net_if_addrs, mock_system):
    mock_net_if_addrs.return_value = {
        "Ethernet": [MagicMock(family=socket.AF_INET, address="192.168.0.50", netmask="255.255.255.0")]
    }
    result = get_ipv4_info()
    assert result == "Interface: Ethernet, IP: 192.168.0.50, Type: Dynamic, Connection: Ethernet"


# Positive Test: Windows, Static IP
@patch("platform.system", return_value="Windows")
@patch("psutil.net_if_addrs")
def test_ipv4_info_windows_static_ip(mock_net_if_addrs, mock_system):
    mock_net_if_addrs.return_value = {
        "Ethernet": [MagicMock(family=socket.AF_INET, address="10.0.0.1", netmask="255.255.255.255")]
    }
    result = get_ipv4_info()
    assert result == "Interface: Ethernet, IP: 10.0.0.1, Type: Static, Connection: Ethernet"


# Negative Test: No IPv4 address found
@patch("psutil.net_if_addrs")
def test_ipv4_info_no_ipv4(mock_net_if_addrs):
    mock_net_if_addrs.return_value = {}
    result = get_ipv4_info()
    assert result == "No IPv4 address found."


# Error Handling: Linux file not found
@patch("platform.system", return_value="Linux")
@patch("psutil.net_if_addrs")
@patch("builtins.open", side_effect=FileNotFoundError)
def test_ipv4_info_linux_file_not_found(mock_open, mock_net_if_addrs, mock_system):
    mock_net_if_addrs.return_value = {
        "eth0": [MagicMock(family=socket.AF_INET, address="192.168.1.102", netmask="255.255.255.0")]
    }
    result = get_ipv4_info()
    assert result == "Interface: eth0, IP: 192.168.1.102, Type: Unknown (file not found), Connection: Ethernet"


# Negative Test: Unsupported platform
@patch("platform.system", return_value="Darwin")
@patch("psutil.net_if_addrs")
def test_ipv4_info_unsupported_platform(mock_net_if_addrs, mock_system):
    mock_net_if_addrs.return_value = {
        "eth0": [MagicMock(family=socket.AF_INET, address="192.168.2.1", netmask="255.255.255.0")]
    }
    result = get_ipv4_info()
    assert result == "Interface: eth0, IP: 192.168.2.1, Type: Unknown (platform not supported), Connection: Ethernet"
