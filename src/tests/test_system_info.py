import pytest
from unittest.mock import patch, MagicMock

from modules.system_info import get_system_info


# Positive Test: Windows system information
@patch("platform.uname")
@patch("psutil.cpu_count")
@patch("psutil.virtual_memory")
@patch("platform.win32_ver")
def test_get_system_info_windows(mock_win32_ver, mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(system="Windows", release="10", version="10.0", machine="x64")
    mock_cpu_count.return_value = 8
    mock_virtual_memory.return_value = MagicMock(total=16 * 1024 ** 3)
    mock_win32_ver.return_value = ("10", "19042")
    
    result = get_system_info()
    assert result == "System: Windows 10 (Build 19042), x64\nCores: 8\nRAM: 16.0 GB"

# Positive Test: Linux system information
@patch("platform.uname")
@patch("psutil.cpu_count")
@patch("psutil.virtual_memory")
def test_get_system_info_linux(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(system="Linux", release="5.4", version="Ubuntu", machine="x86_64")
    mock_cpu_count.return_value = 4
    mock_virtual_memory.return_value = MagicMock(total=8 * 1024 ** 3)
    
    result = get_system_info()
    assert result == "System: Linux 5.4 Ubuntu, x86_64\nCores: 4\nRAM: 8.0 GB"

# Negative Test: Exception during execution (simulating a failure in psutil)
@patch("platform.uname")
@patch("psutil.cpu_count")
@patch("psutil.virtual_memory")
def test_get_system_info_exception(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(system="Linux", release="5.4", version="Ubuntu", machine="x86_64")
    mock_cpu_count.side_effect = Exception("psutil error")  # Simulating an error
    
    result = get_system_info()
    assert result == "System information could not be determined: psutil error"

# Positive Test: Mocking an unsupported OS (e.g., Darwin for MacOS)
@patch("platform.uname")
@patch("psutil.cpu_count")
@patch("psutil.virtual_memory")
def test_get_system_info_mac(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(system="Darwin", release="19.6", version="macOS", machine="x86_64")
    mock_cpu_count.return_value = 4
    mock_virtual_memory.return_value = MagicMock(total=4 * 1024 ** 3)  # 4GB RAM
    
    result = get_system_info()
    assert result == "System: Darwin 19.6 macOS, x86_64\nCores: 4\nRAM: 4.0 GB"

