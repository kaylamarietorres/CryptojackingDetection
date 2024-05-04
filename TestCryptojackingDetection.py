import unittest
from unittest.mock import patch, MagicMock
import CryptojackingDetection

class TestCryptojackingDetection(unittest.TestCase):

    @patch('CryptojackingDetection.psutil.process_iter')
    @patch('CryptojackingDetection.psutil.virtual_memory')
    @patch('CryptojackingDetection.psutil.cpu_percent')
    def test_detection_of_known_mining_process(self, mock_cpu, mock_memory, mock_process_iter):
        # Setup mock values
        mock_cpu.return_value = 5  # Low CPU usage
        mock_memory.return_value = MagicMock(percent=5)  # Low memory usage
        process_mock = MagicMock(name='xmrig', cpu_percent=5, memory_percent=5, pid=1234)
        mock_process_iter.return_value = [process_mock]

        # Run the CPU and Memory check function
        with self.assertLogs('CryptojackingDetection', level='INFO') as log:
            CryptojackingDetection.check_high_resource_usage(duration=1)  # Reduce duration for testing

        # Check logs for expected output
        expected_message = '**Known mining process detected** PID: 1234, Name: xmrig'
        self.assertTrue(any(expected_message in message for message in log.output))

    @patch('CryptojackingDetection.psutil.process_iter')
    @patch('CryptojackingDetection.psutil.virtual_memory')
    @patch('CryptojackingDetection.psutil.cpu_percent')
    def test_high_cpu_usage(self, mock_cpu, mock_memory, mock_process_iter):
        # Setup mock values
        mock_cpu.return_value = 70  # Simulate high CPU usage
        mock_memory.return_value = MagicMock(percent=30)  # Normal memory usage
        process_mock = MagicMock(spec=['info'],
                                 info={'name': 'xmrig', 'cpu_percent': 5, 'memory_percent': 5, 'pid': 1234})
        mock_process_iter.return_value = [process_mock]

        # Ensure that the function logs at WARNING level correctly
        with self.assertLogs('CryptojackingDetection', level='WANRING') as log:
            CryptojackingDetection.check_high_resource_usage(duration=1)  # Reduce duration for testing

        # Check logs for expected output
        expected_message = 'High CPU usage: 70%, Memory usage: 30%'
        self.assertTrue(any(expected_message in message for message in log.output))

    if __name__ == '__main__':
        unittest.main()