from fastapi import FastAPI


app = FastAPI(
    title="Legal RAG API"
)


@app.get("/health")
def health():

    return {
        "status":"healthy"
    }