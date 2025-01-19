import pytest
from unittest.mock import patch, MagicMock

from modules.bios_info import get_bios_version


# Positive Test: Windows BIOS information
@patch("platform.system", return_value="Windows")
@patch("subprocess.check_output")
def test_get_bios_version_windows(mock_subprocess, mock_platform):
    mock_subprocess.return_value = "1.2.3.4"
    result = get_bios_version()
    assert result == "BIOS version: 1.2.3.4"

# Positive Test: Linux BIOS information
@patch("platform.system", return_value="Linux")
@patch("subprocess.check_output")
def test_get_bios_version_linux(mock_subprocess, mock_platform):
    mock_subprocess.return_value = """
    BIOS Information
    Vendor: American Megatrends Inc.
    Version: 2.20
    Release Date: 10/04/2021
    """
    result = get_bios_version()
    assert result == "BIOS version: 2.20"

# Positive Test: macOS BIOS information
@patch("platform.system", return_value="Darwin")
@patch("subprocess.check_output")
def test_get_bios_version_macos(mock_subprocess, mock_platform):
    mock_subprocess.return_value = """
    Hardware:
        Boot ROM Version: 202.0.0.0
    """
    result = get_bios_version()
    assert result == "BIOS version: 202.0.0.0"

# Test for unsupported OS
@patch("platform.system", return_value="FreeBSD")
def test_get_bios_version_unsupported_os(mock_platform):
    result = get_bios_version()
    assert result == "Unsupported OS for BIOS version detection"

# Test for Windows: no output from PowerShell
@patch("platform.system", return_value="Windows")
@patch("subprocess.check_output")
def test_get_bios_version_windows_no_output(mock_subprocess, mock_platform):
    mock_subprocess.return_value = ""
    result = get_bios_version()
    assert result == "BIOS version could not be determined"

# Test for Linux: no "Version" field in `dmidecode`
@patch("platform.system", return_value="Linux")
@patch("subprocess.check_output")
def test_get_bios_version_linux_no_version(mock_subprocess, mock_platform):
    mock_subprocess.return_value = """
    BIOS Information
    Vendor: American Megatrends Inc.
    Release Date: 10/04/2021
    """
    result = get_bios_version()
    assert result == "BIOS version could not be determined"

# Test for Windows: subprocess raises an exception
@patch("platform.system", return_value="Windows")
@patch("subprocess.check_output", side_effect=Exception("Subprocess error"))
def test_get_bios_version_windows_exception(mock_subprocess, mock_platform):
    result = get_bios_version()
    assert result == "BIOS version could not be determined: Subprocess error"

# Test for Linux: subprocess raises an exception
@patch("platform.system", return_value="Linux")
@patch("subprocess.check_output", side_effect=Exception("Subprocess error"))
def test_get_bios_version_linux_exception(mock_subprocess, mock_platform):
    result = get_bios_version()
    assert result == "BIOS version could not be determined: Subprocess error"

# Test for macOS: subprocess raises an exception
@patch("platform.system", return_value="Darwin")
@patch("subprocess.check_output", side_effect=Exception("Subprocess error"))
def test_get_bios_version_macos_exception(mock_subprocess, mock_platform):
    result = get_bios_version()
    assert result == "BIOS version could not be determined: Subprocess error"
