import pika

import pika
import json
import sys
from socket import gaierror
try:
    credentials = pika.PlainCredentials("sid", "test")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   credentials=credentials))
except gaierror as e:
    print("")
channel = connection.channel()
#message = ' '.join(sys.argv[1:]) or "Hello World!"
message = {"id":"123"}
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
"""
credentials = pika.PlainCredentials("sid", "test")
#Create a new instance of the Connection object
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
#Create a new channel with the next available channel number or pass in a channel number to use
channel = connection.channel()
#Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
channel.queue_declare(queue='sample_2', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_publish(exchange='', routing_key='sample_2', body='Hello World!', properties=pika.BasicProperties(
                         delivery_mode=2, # make message persistent
                      ))    
print("[x] Sent 'Hello World!'")
connection.close()
"""
