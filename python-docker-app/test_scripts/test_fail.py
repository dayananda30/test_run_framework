#!/usr/bin/env python
import unittest

class FailTest(unittest.TestCase):

    def test_failure_case(self):
        self.assertTrue(False)

    def test_failure_case_2(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()  
