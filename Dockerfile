FROM python:slim

RUN mkdir /yamdb

COPY requirements.txt /yamdb

RUN pip install -r /yamdb/requirements.txt

COPY . /yamdb

WORKDIR /yamdb

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
