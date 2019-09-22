import pika
import pika
import json
import sys
from socket import gaierror
from functions import get_config
from os.path import dirname, abspath

current_dir = dirname(abspath(__file__))


def publish_test(test_id):
    config_path = current_dir+"/config.yaml"
    rbmq_username = get_config("RABBITMQ_SERVER_DETAILS", "USERNAME", config_path)
    rbmq_password = get_config("RABBITMQ_SERVER_DETAILS", "PASSWORD", config_path)
    rbmq_ip = get_config("RABBITMQ_SERVER_DETAILS", "SERVER_IP", config_path)
    try:
        credentials = pika.PlainCredentials(rbmq_username, rbmq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rbmq_ip,
                                                                       credentials=credentials))
    except gaierror as e:
        print("")
    channel = connection.channel()
    #message = ' '.join(sys.argv[1:]) or "Hello World!"
    message = {"id":test_id}
    channel.queue_declare(queue='test_run.jobs.queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.exchange_declare(exchange='test_run_jobs',
                             exchange_type='topic')
    channel.queue_bind(exchange="test_run_jobs",
                       queue="test_run.jobs.queue",
                       routing_key="hello.#")
    channel.basic_publish(exchange='test_run_jobs',
                          routing_key='hello.hi.how',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                          ))
    print(" [x] Sent {}".format(json.dumps(message)))
    connection.close()
#publish_test(123)
