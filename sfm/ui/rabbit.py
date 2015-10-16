from django.apps import AppConfig
import pika
import os


class RabbitWorker(AppConfig):
    name = 'ui'
    verbose_name = "UI"
    # Create a connection
    credentials = pika.PlainCredentials(
        username=os.environ['MQ_ENV_RABBITMQ_DEFAULT_USER'],
        password=os.environ['MQ_ENV_RABBITMQ_DEFAULT_PASS'])
    parameters = pika.ConnectionParameters(host='mq', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    # create channel
    channel = connection.channel()

    def ready(self):
        # Declare sfm_exchange
        RabbitWorker.channel.exchange_declare(exchange="sfm_exchange",
                                              type="topic", durable=True)
        pass  # startup code here
