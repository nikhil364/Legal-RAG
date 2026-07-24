import os
import time
import json
import pika

from dotenv import load_dotenv

from embedder import generate_embedding
from qdrant_store import store_vector


load_dotenv()



def connect_rabbitmq():

    while True:

        try:

            credentials = pika.PlainCredentials(

                os.getenv("RABBITMQ_USER"),

                os.getenv("RABBITMQ_PASSWORD")

            )


            connection = pika.BlockingConnection(

                pika.ConnectionParameters(

                    host=os.getenv(
                        "RABBITMQ_HOST",
                        "rabbitmq"
                    ),

                    port=int(
                        os.getenv(
                            "RABBITMQ_PORT",
                            5672
                        )
                    ),

                    credentials=credentials,

                    heartbeat=60

                )

            )


            print(
                "Connected to RabbitMQ", flush=True

            )


            return connection


        except Exception as e:

            print(
                "RabbitMQ unavailable, retrying...",
                e
            )

            time.sleep(5)



def start():

    connection = connect_rabbitmq()


    channel = connection.channel()


    channel.queue_declare(
        queue="document_chunks",
        durable=True
    )



    def callback(
        ch,
        method,
        properties,
        body
    ):

        try:

            data = json.loads(body)


            print(
                "Received:",
                data["filename"],
                "page",
                data.get("page")
            )


            vector = generate_embedding(
                data["text"]
            )


            store_vector(
                vector,
                data
            )


            print(
                "Indexed:",
                data["filename"]
            )


            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )


        except Exception as e:

            print(
                "Processing failed:",
                e
            )

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )



    channel.basic_qos(
        prefetch_count=1
    )


    channel.basic_consume(

        queue="document_chunks",

        on_message_callback=callback

    )


    print(
        "Embedding worker started. Waiting for messages..."
    )


    channel.start_consuming()