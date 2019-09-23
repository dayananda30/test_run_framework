import pika

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
