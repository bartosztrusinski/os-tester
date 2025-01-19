import pytest
import socket
import subprocess
from unittest.mock import patch, MagicMock

from modules.network_info import get_ipv4_info

# Positive test case for Linux with static IP
@patch('platform.system', return_value='Linux')
@patch('psutil.net_if_addrs')
@patch('builtins.open')
def test_get_ipv4_info_linux_static(mock_open, mock_net_if_addrs, mock_platform_system):
    mock_net_if_addrs.return_value = {
        'eth0': [MagicMock(family=socket.AF_INET, address='192.168.1.100', netmask='255.255.255.0')]
    }
    
    mock_open.return_value.__enter__.return_value.read.return_value = 'iface eth0 inet static\n'

    result = get_ipv4_info()

    assert "Interface: eth0" in result
    assert "IP: 192.168.1.100" in result
    assert "Type: Static" in result


# Positive test case for Linux with dynamic IP
@patch('platform.system', return_value='Linux')
@patch('psutil.net_if_addrs')
@patch('builtins.open')
def test_get_ipv4_info_linux_dynamic(mock_open, mock_net_if_addrs, mock_platform_system):
    mock_net_if_addrs.return_value = {
        'eth0': [MagicMock(family=socket.AF_INET, address='192.168.1.100', netmask='255.255.255.0')]
    }

    mock_open.return_value.__enter__.return_value.read.return_value = 'iface eth0 inet dhcp\n'

    result = get_ipv4_info()

    assert "Interface: eth0" in result
    assert "IP: 192.168.1.100" in result
    assert "Type: Dynamic" in result


# Positive test case for Windows with dynamic IP
@patch('platform.system', return_value='Windows')
@patch('psutil.net_if_addrs')
def test_get_ipv4_info_windows_dynamic(mock_net_if_addrs, mock_platform_system):
    mock_net_if_addrs.return_value = {
        'eth0': [MagicMock(family=socket.AF_INET, address='192.168.1.100', netmask='255.255.255.0')]
    }
    
    result = get_ipv4_info()
    
    assert "Interface: eth0" in result
    assert "IP: 192.168.1.100" in result
    assert "Type: Dynamic" in result


# Positive test case for macOS with static IP
@patch('platform.system', return_value='Darwin')
@patch('psutil.net_if_addrs')
@patch('subprocess.check_output')
def test_get_ipv4_info_mac_static(mock_subprocess, mock_net_if_addrs, mock_platform_system):
    mock_net_if_addrs.return_value = {
        'eth0': [MagicMock(family=socket.AF_INET, address='192.168.1.100', netmask='255.255.255.0')]
    }
    
    mock_subprocess.return_value = 'inet 192.168.1.100 netmask 255.255.255.0'
    
    result = get_ipv4_info()
    
    assert "Interface: eth0" in result
    assert "IP: 192.168.1.100" in result
    assert "Type: Static" in result


# Negative test case (FileNotFoundError handling for Linux)
@patch('platform.system', return_value='Linux')
@patch('psutil.net_if_addrs')
@patch('builtins.open', side_effect=FileNotFoundError)
def test_get_ipv4_info_linux_file_not_found(mock_open, mock_net_if_addrs, mock_platform_system):
    mock_net_if_addrs.return_value = {'eth0': [MagicMock(family=socket.AF_INET, address='192.168.1.100', netmask='255.255.255.0')]}
    
    result = get_ipv4_info()
    
    assert "Type: Dynamic" in result


# Negative test case (subprocess.CalledProcessError handling for macOS)
@patch('platform.system', return_value='Darwin')
@patch('psutil.net_if_addrs')
@patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'ifconfig'))
def test_get_ipv4_info_mac_subprocess_error(mock_subprocess, mock_net_if_addrs, mock_platform_system):
    mock_net_if_addrs.return_value = {'eth0': [MagicMock(family=socket.AF_INET, address='192.168.1.100', netmask='255.255.255.0')]}
    
    result = get_ipv4_info()
    
    assert "Type: Unknown (error checking IP)" in result