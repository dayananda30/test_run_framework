import pika

import pika
import json
import sys
from socket import gaierror

def publish_test(test_id):
    try:
        credentials = pika.PlainCredentials("sid", "test")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
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
