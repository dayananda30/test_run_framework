import subprocess
import tempfile

def test_runner_for_python(scripts_path):
    cmd = "pytest "+ scripts_path +" -v"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True, encoding='utf-8')
    output = p.stdout.read()
    print(output, type(output))
    print("*************")
    last_line = output.strip().split("\n")[-1]
    last_line = last_line.replace("=", "")
    results = last_line.split(",")
    print(results)

test_runner_for_python("/home/sheetal/tests")
