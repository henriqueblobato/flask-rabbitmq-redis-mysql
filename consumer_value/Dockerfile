FROM python:3.6

RUN pip install pika
WORKDIR /usr/src/app/consumer
COPY lambda_handler.py .
RUN ls -lah /usr/src/app/consumer

ENV PYTHONUNBUFFERED=1
CMD [ "python", "lambda_handler.py" ]
