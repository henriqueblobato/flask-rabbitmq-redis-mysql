from flask import Flask, request, Response
from adapters.redis_adapter import RedisAdapter
from adapters.rabbitmq_adapter import RabbitMqAdapter


import json
from uuid import uuid4

from exceptions import CreditRequestException

app = Flask(__name__)
rabbitmq = RabbitMqAdapter()
channel = rabbitmq.get_channel

PERMITTED_TYPES = [
    'application/json'
]


@app.route('/credit-request', methods=['POST'])
def credit_request():
    try:
        if request.headers.get('CONTENT_TYPE') not in PERMITTED_TYPES:
            raise CreditRequestException('Content type not available')

        data = json.loads(request.data)
        age = data.get('age')
        value = data.get('value')

        ticket_number = str(uuid4())
        response_age = put_on_queue(age, ticket_number)
        response_value = put_on_queue(value, ticket_number)

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
            return Response(
                response='Error in one of the values',
                status=400
            )

    except Exception as e:
        return Response(
            response='Invalid request',
            status=400
        )


def put_on_queue(queue='', ticket=None, payload=''):
    if not queue or not payload:
        return False
    try:
        channel.basic_publish(exchange='exchange_1',
                              routing_key=queue,
                              body=json.dumps({'ticket': ticket, 'value': payload})
                              )
        print(f'[LOG] {payload} on queue {queue}')
        return True
    except Exception:
        return False


if __name__ == "__main__":
    app.run(
        #debug=False,
        port=8000,
        host='0.0.0.0'
    )
