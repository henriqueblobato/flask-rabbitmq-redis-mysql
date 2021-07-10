from flask import Flask, request, Response
import os
import pika
from time import sleep

import json
from uuid import uuid4

from exceptions import CreditRequestException


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
age_queue = channel.queue_declare(queue='age', durable=True)
value_queue = channel.queue_declare(queue='value', durable=True)


app = Flask(__name__)

PERMITTED_TYPES = [
    'application/json'
]


@app.route('/', methods=['GET'])
def health_check():
    return Response(
        response=json.dumps({'Im': 'Alive'}),
        status=200
    )


@app.route('/credit-request', methods=['POST'])
def credit_request():
    try:
        if request.headers.get('CONTENT_TYPE') not in PERMITTED_TYPES:
            raise CreditRequestException('Content type not available')

        data = json.loads(request.data)
        age = data.get('age')
        value = data.get('value')

        ticket_number = str(uuid4())
        response_age = put_on_queue(queue='age', ticket=ticket_number, payload=age)
        response_value = put_on_queue(queue='value', ticket=ticket_number, payload=value)

        if response_age and response_value:
            response = {
                'ticket': ticket_number,
                'message': 'Your request is now being processed'
            }
            return Response(
                response=json.dumps(response),
                status=200
            )
        else:
            raise CreditRequestException(f'Status of request. '
                                         f'age:{response_age}, '
                                         f'value:{response_value}')

    except Exception as e:
        return Response(
            response=str(format(e)),
            status=400
        )


def put_on_queue(queue='', ticket=None, payload=''):
    if not queue or not payload:
        return False
    try:
        payload = json.dumps({'ticket': ticket, 'value': payload})
        channel.basic_publish(exchange='',
                              routing_key=queue,
                              body=payload
                              )
        print(f"{payload} published on queue '{queue}' with success")
        return True
    except Exception as e:
        print(f'{type(e)} on publishing {payload} on '
              f'queue {queue} {str(format(e))}')
        return False


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000,
        host='0.0.0.0'
    )
