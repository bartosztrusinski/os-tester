import unittest
from unittest.mock import patch, MagicMock
from services.system_info import get_system_info

class TestSystemInfo(unittest.TestCase):

    @patch('platform.uname')
    @patch('psutil.cpu_count')
    @patch('psutil.virtual_memory')
    def test_get_system_info(self, mock_virtual_memory, mock_cpu_count, mock_uname):
        mock_uname.return_value = MagicMock(system='Linux', release='5.4', version='5.4.0', machine='x86_64')
        mock_cpu_count.return_value = 4
        mock_virtual_memory.return_value = MagicMock(total=8 * 1024 ** 3)  # 8 GB

        result = get_system_info()
        self.assertIn("System: Linux 5.4 5.4.0, x86_64", result)
        self.assertIn("Cores: 4", result)
        self.assertIn("RAM: 8.0 GB", result)

    @patch('subprocess.check_output')
    def test_get_bios_version_windows(self, mock_check_output):
        mock_check_output.return_value = "1.0.0"
        with patch('platform.system', return_value='Windows'):
            result = get_bios_version()
            self.assertEqual(result, "BIOS version: 1.0.0")

    @patch('subprocess.check_output')
    def test_get_bios_version_linux(self, mock_check_output):
        mock_check_output.return_value = "Version: 1.0.0"
        with patch('platform.system', return_value='Linux'):
            result = get_bios_version()
            self.assertEqual(result, "BIOS version: Version: 1.0.0")

    @patch('socket.gethostname')
    def test_get_host_name(self, mock_gethostname):
        mock_gethostname.return_value = "test-host"
        result = get_host_name()
        self.assertEqual(result, "Host Name: test-host")

if __name__ == '__main__':
    unittest.main()
