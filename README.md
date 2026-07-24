# 📚 Legal RAG (Retrieval-Augmented Generation) System

A distributed, Docker-based Retrieval-Augmented Generation (RAG) system for continuously ingesting, indexing, and querying large collections of legal PDF documents.

This project automatically monitors a directory of legal documents, extracts and chunks PDF content, generates vector embeddings, stores them in Qdrant, and provides an AI-powered chat API capable of answering questions with document citations.

---

# Features

- Automatic PDF ingestion
- Recursive folder monitoring
- Dynamic folder taxonomy extraction
- Incremental document processing
- Asynchronous processing using RabbitMQ
- Semantic vector search using Qdrant
- Local LLM inference using Ollama
- FastAPI REST API
- Dockerized microservice architecture
- Easily scalable embedding workers
- Source-aware answers with citations

---

# Architecture

```
                    +----------------------+
                    |      PDF Dataset     |
                    | docs/...             |
                    +----------+-----------+
                               |
                               |
                    Watchdog File Monitor
                               |
                               v
                  +-------------------------+
                  |     rag-ingestion       |
                  |-------------------------|
                  | • Detect new PDFs       |
                  | • Extract metadata      |
                  | • Chunk documents       |
                  | • Calculate file hash   |
                  +------------+------------+
                               |
                               |
                        RabbitMQ Queue
                      document_chunks
                               |
                               |
                               v
                  +-------------------------+
                  |     rag-embedding       |
                  |-------------------------|
                  | • Generate embeddings   |
                  | • Store vectors         |
                  | • Attach metadata       |
                  +------------+------------+
                               |
                               |
                               v
                      +----------------+
                      |    Qdrant      |
                      | Vector Store   |
                      +-------+--------+
                              |
                              |
                              v
                    +---------------------+
                    |      rag-api        |
                    |---------------------|
                    | • Embed question    |
                    | • Retrieve vectors  |
                    | • Build prompt      |
                    | • Query Ollama      |
                    +----------+----------+
                               |
                               |
                               v
                          AI Response
                      + Source Citations
```

---

# Project Structure

```
legal-rag/

│
├── docs/
│   ├── computer_law/
│   ├── international_law/
│   └── ...
│
├── ingestion/
│
├── embedding/
│
├── rag-api/
│
├── ollama/
│
├── docker-compose.yml
│
└── .env
```

---

# Dataset Organization

The dataset can contain any number of nested folders.

Example:

```
docs/

├── computer_law/
│      ├── europe/
│      │      cyber_act.pdf
│      │
│      └── canada/
│             pipeda.pdf
│
├── international_law/
│      treaties.pdf
│
└── constitutional_law/
       charter.pdf
```

The folder hierarchy is automatically converted into searchable metadata.

Example metadata:

```json
{
  "filepath": "computer_law/europe/cyber_act.pdf",
  "folder_path": [
    "computer_law",
    "europe"
  ],
  "root_category": "computer_law",
  "parent_category": "europe",
  "depth": 2
}
```

No manual categorization is required.

---

# Components

## 1. Ingestion Service

Responsibilities:

- Watches dataset directory
- Detects newly added PDFs
- Detects modified PDFs
- Extracts document text
- Splits into chunks
- Generates metadata
- Publishes chunks to RabbitMQ

Metadata includes:

- filename
- filepath
- folder hierarchy
- root category
- parent category
- page number
- document hash

---

## 2. RabbitMQ

RabbitMQ decouples ingestion from embedding generation.

Advantages:

- asynchronous processing
- fault tolerance
- scalable workers
- queue persistence

Queue:

```
document_chunks
```

---

## 3. Embedding Service

Responsibilities:

- Consumes RabbitMQ messages
- Generates sentence embeddings
- Stores vectors in Qdrant
- Preserves metadata

Embedding model:

```
BAAI/bge-small-en-v1.5
```

---

## 4. Qdrant

Stores:

- embeddings
- chunk text
- metadata
- page numbers
- folder taxonomy

Example payload:

```json
{
  "filename": "cyber_act.pdf",
  "page": 45,
  "text": "...",
  "folder_path": [
    "computer_law",
    "europe"
  ]
}
```

---

## 5. API Service

FastAPI provides:

### Health

```
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

---

### Semantic Search

```
POST /search
```

Example:

```json
{
  "query":"European cybersecurity law",
  "top_k":5
}
```

Returns:

```json
{
  "results":[
      ...
  ]
}
```

---

### AI Chat

```
POST /ask
```

Example:

```json
{
  "query":"What cybersecurity obligations exist under European computer law?",
  "top_k":5
}
```

Returns:

```json
{
    "answer":"...",
    "sources":[...]
}
```

---

## 6. Ollama

Runs the local LLM.

Current model:

```
llama3.1
```

The model is automatically downloaded during container startup if it is not already available.

---

# Getting Started

## Clone

```bash
git clone <repository>

cd legal-rag
```

---

## Configure

Create:

```
.env
```

Example:

```env
POSTGRES_DB=ragdb
POSTGRES_USER=rag
POSTGRES_PASSWORD=password

RABBITMQ_USER=rag
RABBITMQ_PASSWORD=password

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
```

---

## Build

```bash
docker compose build
```

---

## Start

```bash
docker compose up
```

All services start automatically:

- PostgreSQL
- RabbitMQ
- Qdrant
- Ollama
- Ingestion
- Embedding
- API

---

# Adding Documents

Simply copy PDFs into the dataset.

Example:

```
docs/

└── computer_law/

      └── europe/

            cyber_act.pdf
```

The ingestion service automatically:

1. Detects file
2. Chunks document
3. Publishes to RabbitMQ
4. Generates embeddings
5. Stores vectors

No restart required.

---

# Example Query

```bash
curl -X POST \
http://localhost:8000/ask \
-H "Content-Type: application/json" \
-d '
{
  "query":"What cybersecurity obligations exist under European computer law?",
  "top_k":5
}
'
```

Example response:

```json
{
  "answer":"...",
  "sources":[
      {
          "filename":"cyber_act.pdf",
          "page":45
      }
  ]
}
```

---

# Technology Stack

| Component | Technology |
|------------|------------|
| API | FastAPI |
| Vector Database | Qdrant |
| Message Broker | RabbitMQ |
| Database | PostgreSQL |
| Embeddings | Sentence Transformers |
| LLM | Ollama |
| Containerization | Docker |
| File Monitoring | Watchdog |
| Language | Python 3.12 |

---

# Future Improvements

- PostgreSQL document registry
- Duplicate detection
- Incremental re-indexing
- Document deletion synchronization
- Hybrid Search (BM25 + Vector)
- Cross-Encoder reranking
- Streaming responses
- Authentication
- React frontend
- Kubernetes deployment
- OpenTelemetry observability
- Prometheus metrics
- Grafana dashboards

---

# License

This project is provided for educational and research purposes.

---

# Acknowledgements

This project was inspired by modern Retrieval-Augmented Generation (RAG) architectures and adapted to support continuously growing legal document collections using a scalable, event-driven microservice design.