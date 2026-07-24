from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)


client = QdrantClient(
    host="qdrant",
    port=6333
)


COLLECTION = "documents"



def create_collection():

    print("Initializing Qdrant...")

    collections = (
        client.get_collections()
        .collections
    )


    print("Qdrant connected")

    existing = [
        c.name
        for c in collections
    ]


    if COLLECTION not in existing:

        client.create_collection(

            collection_name=COLLECTION,

            vectors_config=VectorParams(

                size=384,

                distance=Distance.COSINE
            )
        )


        print(
            "Created Qdrant collection"
        )



def store_vector(vector, payload):

    import uuid


    point = PointStruct(

        id=str(uuid.uuid4()),

        vector=vector,

        payload=payload

    )


    client.upsert(

        collection_name=COLLECTION,

        points=[point]

    )