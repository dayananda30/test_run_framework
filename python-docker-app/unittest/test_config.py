#import usertest
#import configtest # first test
import unittest   # second test

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        print('stp')
        ##set up code

    def runTest(self):
        #runs test
        print ('stp')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

'''
def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ConfigTestCase))
    return test_suite

mySuit=suite()

runner=unittest.TextTestRunner()
a = runner.run(mySuit)
print(a)
print(dir(a))
'''
