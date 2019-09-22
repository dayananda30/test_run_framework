import os
import subprocess
import errno
import shutil

import yaml


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


def test_runner_for_python(scripts_path):
    cmd = "pytest "+ scripts_path +" -v"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, close_fds=True, encoding='utf-8')
    output = p.stdout.read()
#    print(output, type(output))
#    print("*************")
#    last_line = output.strip().split("\n")[-1]
#    last_line = last_line.replace("=", "")
#    results = last_line.split(",")
#    print(results)
    return output  
    #return last_line
#    with open("/src/test_results",'w') as file_hd:
#        for each_line in output.strip().split("\n"):
#        file_output.write(each_line)


#copy("/home/sheetal/tests", "/home/sheetal/dummy")
#delete_folder("/home/sheetal/dummy")
