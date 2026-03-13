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
    port=5674,
    credentials=credentials
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f"[{method.routing_key}] Получено: {body}")


channel.basic_consume(queue='quorum', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
