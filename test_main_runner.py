import unittest
from mock import patch
from os.path import dirname, abspath, join, exists
from mock import MagicMock
import sys
current_dir = dirname(dirname(abspath(__file__)))

sys.path.append(current_dir)

import main_runner
class TestMainRunner(unittest.TestCase):

    @patch('main_runner.functions.copy')
    @patch('main_runner.publisher.publish_test')
    @patch('main_runner.postgre_model.db.DBSession.session_close')
    @patch('main_runner.postgre_model.db.DBSession.create_entry')
    @patch('main_runner.time.sleep', return_value=None)
    def test_main_runtest_option(self, sleep_mock, create_id_mock, session_close_mock,
                                 publish_test_mock, copy_mock):
        create_id_mock.return_value = 1
        session_close_mock.return_value = None
        copy_mock.return_value = None
        publish_test_mock.return_value = None
        user_input = [
            '1',
            '',
        ]
        expected_stacks = "Test execution started and test id - 1"
        with patch('builtins.input', side_effect=user_input):
            stacks = main_runner.main()
        print(stacks)
        self.assertEqual(stacks, expected_stacks)
