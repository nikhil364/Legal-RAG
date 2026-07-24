import pika
import json
import time
import os

from dotenv import load_dotenv

load_dotenv()


RABBIT_USER=os.getenv(
    "RABBITMQ_USER"
)

RABBIT_PASSWORD=os.getenv(
    "RABBITMQ_PASSWORD"
)

RABBIT_HOST=os.getenv(
    "RABBITMQ_HOST",
    "rabbitmq"
)

def create_connection():

    while True:

        try:

            credentials = pika.PlainCredentials(
                RABBIT_USER,
                RABBIT_PASSWORD
            )


            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    credentials=credentials,
                    heartbeat=60,
                    blocked_connection_timeout=300
                )
            )


            print(
                "RabbitMQ connected"
            )

            return connection


        except Exception as e:

            print(
                "RabbitMQ unavailable:",
                e
            )

            time.sleep(5)



def send_chunk(chunk):

    while True:

        try:

            connection = create_connection()

            channel = connection.channel()


            channel.queue_declare(
                queue="document_chunks",
                durable=True
            )


            channel.basic_publish(

                exchange="",

                routing_key="document_chunks",

                body=json.dumps(chunk),

                properties=pika.BasicProperties(
                    delivery_mode=2
                )

            )


            connection.close()


            print(
                "Chunk sent:",
                chunk["filename"],
                "page",
                chunk["page"]
            )


            break


        except Exception as e:

            print(
                "Publish failed:",
                e
            )

            time.sleep(5)