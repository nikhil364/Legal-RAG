from consumer import start
from qdrant_store import create_collection

if __name__=="__main__":

    print("Starting embedding service")

    create_collection()

    start()