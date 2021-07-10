FROM python:3.6

WORKDIR /usr/src/app/worker
COPY app.py .
COPY exceptions.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN ls -lah /usr/src/app/worker

EXPOSE 8000

ENV FLASK_APP = /usr/src/app/worker/app.py
ENV PYTHONUNBUFFERED=1
#ENV SERVER_NAME = '0.0.0.0'

#CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["python", "app.py"]
#CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]