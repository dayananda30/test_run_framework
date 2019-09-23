import unittest
from mock import patch
import functions 

from mock import MagicMock

class TestFunctions(unittest.TestCase):

    @patch('functions.shutil.rmtree')
    def test_delete_folder(self, rm_mock):
        rm_mock.return_value = True
        path = '/home/sheetal/dm_dir'
        result = functions.delete_folder(path)
        self.assertEqual(result, None)

    @patch('functions.shutil.copytree')
    def test_copy_folder(self, copy_mock):
        copy_mock.return_value = True
        src_path = '/home/sheetal/no_folder'
        dest_path = '/home/sheetal/dm_dir'
        result = functions.copy(src_path, dest_path)
        self.assertEqual(result, None)

    def test_copy_folder_not_src_folder(self):
        src_path = '/home/sheetal/no_folder'
        dest_path = '/home/sheetal/dm_dir'
        result = functions.copy(src_path, dest_path)
        self.assertEqual(result, None)

    def test_get_config(self):
        config_path = "tests/dummy_config.yaml"
        rbmq_username = functions.get_config("RABBITMQ_SERVER_DETAILS", "USERNAME", config_path)
        self.assertEqual(rbmq_username, "sid")

    def test_get_config_no_key(self):
        config_path = "tests/dummy_config.yaml"
        with self.assertRaises(Exception) as context:
            rbmq_port = functions.get_config("RABBITMQ_SERVER_DETAILS", "PORT", config_path)
            self.assertTrue("An exception occured" in str(context.exception))

    def test_get_config_value_is_not_set(self):
        config_path = "tests/dummy_config.yaml"
        with self.assertRaises(Exception) as context:
            rbmq_port = functions.get_config("RABBITMQ_SERVER_DETAILS", "SERVER_IP", config_path)
            self.assertTrue("An exception occured" in str(context.exception))
