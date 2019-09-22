print("Hello Python")
import yaml
import subprocess
from postgre_models.models import setup_db 
from os.path import dirname, abspath, join, exists

current_dir = dirname(abspath(__file__))

def read_config_yaml(file_path):
    with open(file_path) as f:
        data = yaml.load(f)
    return data

def update_config_yaml(data, file_path):
    with open(file_path, 'w') as f:
        data = yaml.dump(data, f, default_flow_style=False)

def setup():
    file_path = current_dir+"/config.yaml"
    data = read_config_yaml(file_path)
    #get Postgres DB IP
    cmd = 'sudo docker inspect my_postgres2 | grep -iw "IPADDress"'
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, close_fds=True, encoding='utf-8')
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        psql_ip = stdout.split('\n')
        psql_ip = psql_ip[0].split(':')[1]
        psql_ip = psql_ip.strip(',').strip(' ').strip('"').strip('"')
    else:
        print("Not able to fetch Postgres Database Server IP Address, setup process failed!!!")
        return
    print(psql_ip)
    #get VM ip for updating rabbitmq.

    cmd = 'sudo hostname -I'
    proc_host = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, close_fds=True, encoding='utf-8')
    stdout, stderr = proc_host.communicate()
    if proc_host.returncode == 0:
        host_ip = stdout.split(' ')
        host_ip = host_ip[0].strip(' ')
    else:
        print("Not able to fetch Host Machine IP Address, setup process failed!!!")
        return
    print(host_ip)
    #write to config.yaml
    data['RABBITMQ_SERVER_DETAILS']['SERVER_IP'] = host_ip
    data['POSTGRES_DB_DETAILS']['SERVER_IP'] = psql_ip 
    update_config_yaml(data, file_path)
    #Configure Database, do this after updating of config.yaml 
    setup_db()

setup()
