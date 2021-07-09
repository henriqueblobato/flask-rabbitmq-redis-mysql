FROM python:3.6

RUN pip install pipenv
#RUN apt-get update && apt-get install -y --no-install-recommends gcc
WORKDIR /tmp
COPY .. /tmp
RUN ls -lah /tmp
RUN pip install -r requirements.txt

EXPOSE 8000

ENV FLASK_APP = /tmp/app.py
ENV SERVER_NAME = '0.0.0.0'

CMD ["python", "app.py"]
#CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]