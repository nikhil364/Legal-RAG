from fastapi import FastAPI


from models import SearchRequest

from embeddings import create_embedding

from qdrant_search import search_vectors
from prompt import build_prompt
from llm import generate_answer


app = FastAPI(
    title="RAG Search API"
)



@app.get("/health")
def health():

    return {
        "status":"ok"
    }



@app.post("/search")
def search(
    request: SearchRequest
):

    vector = create_embedding(
        request.query
    )


    results = search_vectors(

        vector,

        request.top_k

    )


    return {

        "query":
            request.query,


        "results":
            results

    }

@app.post("/ask")
def ask(request: SearchRequest):


    vector=create_embedding(
        request.query
    )


    chunks=search_vectors(

        vector,

        request.top_k

    )


    prompt=build_prompt(

        request.query,

        chunks

    )


    answer=generate_answer(
        prompt
    )


    return {

        "answer":answer,

        "sources":[

            c["payload"]

            for c in chunks

        ]

    }

