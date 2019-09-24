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

def test_runner_for_python(scripts_path):
    loader = unittest.TestLoader()
    suite = loader.discover(scripts_path)

    runner = unittest.TextTestRunner()
    a=runner.run(suite)
    details_report = ''

    #print(dir(a))
    #print(a.testsRun, type(a.testsRun))
    pass_count = a.testsRun
    pass_count -= len(a.errors)
    pass_count -= len(a.failures)
    pass_count -= len(a.expectedFailures)
    pass_count -= len(a.skipped)

    out_1 = format_output(a.errors, "ERROR")
    print(out_1)
    out_2 = format_output(a.failures, "FAIL")
    print(out_2)
    print('skipped ', a.skipped)
    print('expected failures ', a.expectedFailures)
    out_3 = format_output(a.expectedFailures, "EXPECTED FAIL")
    out_4 = format_output(a.skipped, "SKIPPED")
    print(out_3)
    print(out_4)
    print(a.testsRun, pass_count)
    #Python scripts test results :  8 failed, 6 passed, 2 skipped, 1 xfailed, 1 xpassed
    last_line = "Python scripts test results : "

import glob
import importlib
import inspect
import os
def get_classes(scripts_path):

    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    current_module_name = os.path.splitext(os.path.basename(current_dir))[0]
    for file in glob.glob(scripts_path+"/test*.py"):
         name = os.path.splitext(os.path.basename(file))[0]

         # Ignore __ files
         if name.startswith("__"):
             continue
         module = importlib.import_module("." + name,package=current_module_name)

         for member in dir(module):
             handler_class = getattr(module, member)

             if handler_class and inspect.isclass(handler_class):
                 print(member)
start_dir = '/home/sheetal/sid/code_space/project_space/test_framework/python-docker-app/test_scripts'
#test_runner_for_python(start_dir)
print(get_classes(start_dir))
