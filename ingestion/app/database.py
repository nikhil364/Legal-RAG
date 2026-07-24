import os
import time

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()



DB_USER = os.getenv(
    "POSTGRES_USER"
)

DB_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD"
)

DB_NAME = os.getenv(
    "POSTGRES_DB"
)

DB_HOST = os.getenv(
    "POSTGRES_HOST",
    "postgres"
)

DB_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432"
)



DATABASE_URL = (
    f"postgresql://"
    f"{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)



while True:

    try:

        engine = create_engine(
            DATABASE_URL
        )


        with engine.connect():

            print(
                "Connected to PostgreSQL"
            )

            break


    except Exception as e:

        print(
            "Waiting for PostgreSQL...",
            e
        )

        time.sleep(5)



SessionLocal = sessionmaker(
    bind=engine
)