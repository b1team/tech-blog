FROM python:3.6-buster

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .


