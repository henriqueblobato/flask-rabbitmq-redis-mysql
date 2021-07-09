import pika


class RabbitMqAdapter:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='exchange_1',
                             exchange_type='fanout')

    age_queue = channel.queue_declare(queue='age',
                                      exclusive=True)
    value_queue = channel.queue_declare(queue='value',
                                        exclusive=True)

    channel.queue_bind(exchange='exchange_1',
                       queue=age_queue.method.queue)
    channel.queue_bind(exchange='exchange_1',
                       queue=value_queue.method.queue)


    @property
    def get_channel(self):
        return self.channel
