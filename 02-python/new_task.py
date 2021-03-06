import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5673))
channel = connection.channel()

# create the "hello" queue
channel.queue_declare(queue="task_queue", durable=True)

message = " ".join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange="", routing_key="task_queue", body=message, properties=pika.BasicProperties(
    delivery_mode=2, # makes messages persistent
    ))

print(" [x] Sent %r" % message)

connection.close()