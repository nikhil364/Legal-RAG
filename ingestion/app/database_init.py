from database import engine
from models import Base


def initialize_database():

    print("Initializing database...")


    Base.metadata.create_all(
        bind=engine
    )


    print(
        "Database initialization complete"
    )