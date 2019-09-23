import unittest   # second test

def format_output(list_tests, status):
    consolidated_output = ""
    for test in list_tests:
        output = """====================================================================== 
{}: {} 
----------------------------------------------------------------------
{}""".format(status, test[0], test[1])
        consolidated_output = "\n".join([consolidated_output, output])
    return consolidated_output

loader = unittest.TestLoader()
start_dir = '/home/sheetal/sid/code_space/project_space/test_framework/python-docker-app/unittest'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
a=runner.run(suite)

print(dir(a))
print(a.testsRun, type(a.testsRun))
print(a.wasSuccessful)
out_1 = format_output(a.errors, "ERROR")
print(out_1)
out_2 = format_output(a.failures, "FAIL")
print(out_2)
