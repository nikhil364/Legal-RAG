from qdrant_client import QdrantClient


client = QdrantClient(
    host="qdrant",
    port=6333
)


COLLECTION = "documents"



def search_vectors(vector, limit=5):

    results = client.query_points(

        collection_name=COLLECTION,

        query=vector,

        limit=limit

    ).points


    output = []


    for result in results:

        output.append({

            "score": result.score,

            "payload": result.payload

        })


    return output