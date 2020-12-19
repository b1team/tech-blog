FROM python:3.6-buster

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && \
    useradd -u 1612 techblog && \
    mkdir /app && \
    chown techblog:techblog /app

USER techblog

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .


