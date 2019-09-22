import pika
import os
import time

print("Step1")
def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()
print("Step2")
credentials = pika.PlainCredentials("sid", "test")
print("Step3")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.116', credentials=credentials))
print("Step4")
channel = connection.channel()
print("Step5")
channel.queue_declare(queue='hello')
print("Step6")

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body) 
    time.sleep(60)
    touch("/src/sheetal")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='sample_1', auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
