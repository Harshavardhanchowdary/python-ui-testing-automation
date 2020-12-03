import os
from unittest import TestCase
from unittest.mock import patch

from ui_automation_core.utilities.log_utils import LogUtils


class LoggingTest(TestCase):

    def test_LogUtils_is_instantiate(self):
        log_dir = '../logs/'
        log_util = LogUtils(log_dir)
        self.assertEqual('An instance of LogUtils is created and `logs` folder is created.', str(log_util))

    @patch('builtins.print')
    def test_create_log_directory(self, mock_print):
        """
        Tests whether `Logs` directory gets created if it does not exist or skips execution if the directory exists.
        :param mock_print:
        :return:
        """
        is_log_folder_exists = os.path.isdir('../logs/')
        log_dir = '../logs/'
        LogUtils(log_dir).create_log_directory()
        if is_log_folder_exists:
            mock_print.assert_called_with('Directory ../logs/  already exists')
        else:
            mock_print.assert_called_with('Directory ../logs/ Created')
