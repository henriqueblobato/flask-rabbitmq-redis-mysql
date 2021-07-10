import pika
import os
from time import sleep
import json

amqp_url = os.environ.get('AMQP_URL')
url_params = pika.URLParameters(amqp_url)
while True:
    try:
        connection = pika.BlockingConnection(url_params)
        print('Connected to rabbitmq')
        break
    except pika.exceptions.AMQPConnectionError:
        print('AMQPConnectionError trying again')
        sleep(5)
        continue

channel = connection.channel()
channel.queue_declare(queue='age', durable=True)


def receive_msg(chan, method, properties, body):
    message = body.decode('utf-8')
    message = json.loads(message)

    value = message.get('value')
    if value and value > 18:
        print(f'{message} allowed')
    else:
        print(f'{message} NOT allowed')

    chan.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='age',
                      on_message_callback=receive_msg)

channel.start_consuming()
