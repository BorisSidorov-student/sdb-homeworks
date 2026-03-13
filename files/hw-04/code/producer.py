#!/usr/bin/env python
# coding=utf-8
import pika
import os
from dotenv import load_dotenv

# Загружаем переменные из .env в окружение
load_dotenv()

RABBIT_HOST=os.getenv('RABBITMQ_HOST')
RABBIT_USER=os.getenv('RABBITMQ_DEFAULT_USER')
RABBIT_PASS=os.getenv('RABBITMQ_DEFAULT_PASS')

# Проверяем, что все переменные загружены
if not all([RABBIT_USER, RABBIT_PASS]):
    raise ValueError("Не удалось загрузить учётные данные из .env")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
parameters = pika.ConnectionParameters(
    host=RABBIT_HOST,
    credentials=credentials
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(
    queue='like',
    durable=True,
    arguments={
        'x-queue-type': 'quorum',
        'x-quorum-initial-group-size': 3
    }
)

channel.basic_publish(exchange='', routing_key='like', body="You've been liked !")
connection.close()