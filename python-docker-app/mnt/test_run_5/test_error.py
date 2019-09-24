import unittest

class ErrorTest(unittest.TestCase):

    def test_error_case(self):
        raise RuntimeError('Test error!')
