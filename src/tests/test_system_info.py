import pytest
from unittest.mock import patch, MagicMock

from modules.system_info import get_system_info


import pytest
from unittest.mock import patch, MagicMock

from modules.system_info import get_system_info


# Positive Test: Check if system info is returned correctly for Windows
@patch('platform.win32_ver')
@patch('psutil.cpu_count', return_value=4)
@patch('psutil.virtual_memory')
def test_get_system_info_windows(mock_virtual_memory, mock_cpu_count, mock_win32_ver):
    mock_win32_ver.return_value = ("10", "10.0.19042", "SP0", "Build 19042")  # Correctly return 4 values
    
    mock_virtual_memory.return_value.total = 16 * 1024**3  # 16 GB RAM

    result = get_system_info()

    expected_result = "System: Windows 10 (Build 10.0.19042), AMD64\nCores: 4\nRAM: 16.0 GB"  # Changed x86_64 to AMD64
    assert result == expected_result


# Positive Test: Check if system info is returned correctly for Linux
@patch('platform.uname')
@patch('psutil.cpu_count', return_value=8)
@patch('psutil.virtual_memory')
def test_get_system_info_linux(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(
        system="Linux",
        release="5.10.0",
        version="5.10.0-8-amd64",
        machine="x86_64"
    )
    mock_virtual_memory.return_value.total = 8 * 1024**3

    result = get_system_info()

    expected_result = "System: Linux 5.10.0 5.10.0-8-amd64, x86_64\nCores: 8\nRAM: 8.0 GB"
    assert result == expected_result


# Positive Test: Check if system info is returned correctly for macOS
@patch('platform.uname')
@patch('psutil.cpu_count', return_value=4)
@patch('psutil.virtual_memory')
def test_get_system_info_macOS(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(
        system="Darwin",
        release="20.3.0",
        version="Darwin Kernel Version 20.3.0",
        machine="x86_64"
    )
    mock_virtual_memory.return_value.total = 16 * 1024**3

    result = get_system_info()

    expected_result = "System: Darwin 20.3.0 Darwin Kernel Version 20.3.0, x86_64\nCores: 4\nRAM: 16.0 GB"
    assert result == expected_result


# Negative Test: When platform system function raises an exception (e.g., unexpected system behavior)
@patch('platform.uname', side_effect=Exception("Platform error"))
def test_get_system_info_platform_error(mock_uname):
    result = get_system_info()
    assert result == "System information could not be determined: Platform error"


# Negative Test: When psutil functions raise exceptions
@patch('platform.uname')
@patch('psutil.cpu_count', side_effect=Exception("psutil CPU count error"))
@patch('psutil.virtual_memory', side_effect=Exception("psutil memory error"))
def test_get_system_info_psutil_error(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(
        system="Linux",
        release="5.10.0",
        version="5.10.0-8-amd64",
        machine="x86_64"
    )
    result = get_system_info()
    assert result == "System information could not be determined: psutil CPU count error"


# Error Test: Check error message when psutil.virtual_memory is unavailable (e.g., mocking a failure)
@patch('platform.uname')
@patch('psutil.cpu_count', return_value=4)
@patch('psutil.virtual_memory', side_effect=AttributeError("virtual_memory not found"))
def test_get_system_info_memory_error(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_uname.return_value = MagicMock(
        system="Linux",
        release="5.10.0",
        version="5.10.0-8-amd64",
        machine="x86_64"
    )
    result = get_system_info()
    assert result == "System information could not be determined: virtual_memory not found"


# Edge Case Test: When CPU count is 0
@patch('platform.uname')
@patch('psutil.cpu_count', return_value=0)
@patch('psutil.virtual_memory')
def test_get_system_info_zero_cores(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_virtual_memory.return_value.total = 16 * 1024**3
    mock_uname.return_value = MagicMock(
        system="Linux",
        release="5.10.0",
        version="5.10.0-8-amd64",
        machine="x86_64"
    )

    result = get_system_info()

    expected_result = "System: Linux 5.10.0 5.10.0-8-amd64, x86_64\nCores: 0\nRAM: 16.0 GB"
    assert result == expected_result


# Edge Case Test: When RAM is 0 GB
@patch('platform.uname')
@patch('psutil.cpu_count', return_value=4)
@patch('psutil.virtual_memory')
def test_get_system_info_zero_ram(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_virtual_memory.return_value.total = 0
    mock_uname.return_value = MagicMock(
        system="Linux",
        release="5.10.0",
        version="5.10.0-8-amd64",
        machine="x86_64"
    )

    result = get_system_info()

    expected_result = "System: Linux 5.10.0 5.10.0-8-amd64, x86_64\nCores: 4\nRAM: 0.0 GB"
    assert result == expected_result


# Error Test: Handle exception gracefully if the system can't determine the platform information
@patch('platform.uname', side_effect=Exception("Unable to determine platform"))
@patch('psutil.cpu_count', return_value=4)
@patch('psutil.virtual_memory')
def test_get_system_info_graceful_error_handling(mock_virtual_memory, mock_cpu_count, mock_uname):
    mock_virtual_memory.return_value.total = 16 * 1024**3

    result = get_system_info()
    assert result == "System information could not be determined: Unable to determine platform"
