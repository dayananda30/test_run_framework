import os
import subprocess
import errno
import shutil
import yaml
import stat
import glob 
import re
import unittest

def get_config(appliance, param, yaml_file_path):
    """This function gives the yaml value corresponding to the parameter
    sample Yaml file
        xstream_details:
            xtm_host: 10.100.26.90
    :param appliance: The header name as mentioned in the yaml file (ex:xstream_details)
    :param param: The parameter name who's value is to be determined (ex: xtm_host)
    :param yaml_file_path: Path of yaml file, Default will the config.yaml file
    :return: value corresponding to the parameter in yaml file
    :except: Exception while opening or loading the file
    """
    try:
        with open(yaml_file_path, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)
        if param is None:
            param_value = doc[appliance]
        else:
            param_value = doc[appliance][param]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param)
            raise ValueError(message)
        return param_value
    except ValueError as ve:
        raise ve
    except Exception as ex:
        message = "Exception: An exception occured: {}".format(ex)
        raise Exception(message)


def delete_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

def get_list_scripts(scripts_path, file_ext):
    return glob.glob(os.path.join(scripts_path, file_ext))

def start_test_execution(scripts_path):
    bash_scripts = get_list_scripts(scripts_path, "*.sh")
    python_scripts = get_list_scripts(scripts_path, "*.py")

    py_test_status = ''
    bash_test_status = ''
    consolidated_output = ''
    if len(python_scripts) > 0 :
        py_test_output = test_runner_for_python(scripts_path)
        last_line = py_test_output.strip().split("\n")[-1]
        py_test_status =  last_line
        py_test_output = py_test_output[:py_test_output.rfind('\n')] 
        consolidated_output = "\n".join([consolidated_output, py_test_output])
    if len(bash_scripts) > 0 :
        bash_test_output = test_runner_for_bash(scripts_path)
        last_line = bash_test_output.strip().split("\n")[-1]
        bash_test_status = last_line 
        bash_test_output = bash_test_output[:bash_test_output.rfind('\n')] 
        consolidated_output = "\n".join([consolidated_output, bash_test_output])

    if py_test_status:
        consolidated_output = "\n".join([consolidated_output, py_test_status])
    if bash_test_status:
        consolidated_output = "\n".join([consolidated_output, bash_test_status])
    return consolidated_output

def test_runner_for_bash(scripts_path):
    list_test_scripts = get_list_scripts(scripts_path, "*.sh")
    consolidated_output = ''
    test_results = {'passed': 0, 'failed': 0}
    if len(list_test_scripts) > 0:
        for script in list_test_scripts:
            st = os.stat(script)
            os.chmod(script, st.st_mode | stat.S_IEXEC)
            cmd = "/bin/sh "+ script 
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, close_fds=True, encoding='utf-8')
            output = p.stdout.read()
            consolidated_output = "\n".join([consolidated_output, output])
            last_line = output.strip().split("\n")[-1]
            last_line = last_line.replace("=", "")
            results = last_line.split(",")
            for each_status in results:
                if "pass" in each_status.lower():
                    pass_count = int(re.search(r'\d+', each_status).group())
                    test_results['passed'] += pass_count
                elif "fail" in each_status.lower():
                    fail_count = int(re.search(r'\d+', each_status).group())
                    test_results['failed'] += fail_count
        bash_test_results = "Bash script test results : "
        flat_results = ', '.join("{!r} {!s}".format(v,k) for (k,v) in test_results.items())
        bash_test_results = bash_test_results + "" + flat_results
        consolidated_output = "\n".join([consolidated_output, bash_test_results])
    return consolidated_output  

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
    list_test_scripts = get_list_scripts(scripts_path, "test*.py")
    details_report = ''
    print(list_test_scripts)
    if len(list_test_scripts) > 0:
        first_line = '======================================================================'
        test_cases  = 'Identified following test scripts:'
        details_report = "\n".join([details_report, first_line, test_cases])
        for test_script in list_test_scripts:
            details_report = "\n".join([details_report, os.path.basename(test_script)])
        test_session = '------------------------- test session ------------------------------'
        details_report = "\n".join([details_report, test_session])
        loader = unittest.TestLoader()
        suite = loader.discover(scripts_path)

        runner = unittest.TextTestRunner()
        a=runner.run(suite)

        test_result = 'Ran {} - '.format(a.testsRun)
        #print(dir(a))
        #print(a.testsRun, type(a.testsRun))
        pass_count = a.testsRun
        pass_count -= len(a.errors)
        pass_count -= len(a.failures)
        pass_count -= len(a.expectedFailures)
        pass_count -= len(a.skipped)

        test_results = "{} passed".format(pass_count)
        err_count = len(a.errors)
        if err_count > 0:
            display_data = format_output(a.errors, "ERROR")
            details_report = "\n".join([details_report, display_data])
        test_results = (', ').join([test_results, "{} error".format(err_count)])

        fail_count = len(a.failures)
        if fail_count > 0:
            display_data = format_output(a.failures, "FAIL")
            details_report = "\n".join([details_report, display_data])
        test_results = (', ').join([test_results, "{} failed".format(fail_count)])

        exp_fail_count = len(a.expectedFailures)
        if exp_fail_count > 0:
            display_data = format_output(a.expectedFailures, "EXPECTED FAIL")
            details_report = "\n".join([details_report, display_data])
            test_results = (', ').join([test_results, "{} expected failures".format(exp_fail_count)])

        skip_count = len(a.skipped)
        if skip_count > 0:
            display_data = format_output(a.skipped, "SKIPPED")
            details_report = "\n".join([details_report, display_data])
            test_results = (', ').join([test_results, "{} skipped".format(skip_count)])

        seperator = "----------------------------------------------------------------------"

        details_report = "\n".join([details_report, seperator])
        details_report = "\n".join([details_report, test_results])
        #Python scripts test results :  8 failed, 6 passed, 2 skipped, 1 xfailed, 1 xpassed
        last_line = "Python scripts test results : {}".format(test_results)
        details_report = "\n".join([details_report, last_line])
    return details_report

#start_dir = '/home/sheetal/sid/code_space/project_space/test_framework/python-docker-app/test_scripts'
#print(start_test_execution(start_dir))
