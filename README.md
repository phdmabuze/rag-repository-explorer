# RAG Repository Explorer

RAG Repository Explorer is a system for indexing source code repositories and searching through them using semantic search and LLM-generated answers.

The project indexes repository files, splits them into chunks, generates embeddings, stores them in PostgreSQL with pgvector, and uses retrieved context to generate answers with a local LLM.

## Features

- Index GitHub repositories
- Split source files into searchable chunks
- Generate embeddings using a separate embedding service
- Store chunks and embeddings in PostgreSQL with pgvector
- Perform semantic search over indexed repositories
- Generate answers using a local LLM

## Architecture

The project is organized as a monorepo containing several services:

- **API** — provides REST endpoints for semantic search and chat with indexed repositories.
- **Indexer** — clones repositories, extracts supported files, splits them into chunks, generates embeddings and stores data in PostgreSQL.
- **Embedding** — standalone service responsible for loading the embedding model and generating vectors.
- **PostgreSQL + pgvector** — stores chunks, metadata and embeddings.
- **Ollama** — provides the local LLM used for generating answers.

## How It Works

1. The indexer reads repositories configured in `sources.json`.

2. The repository is cloned and supported files (`.py`, `.md`, `.yaml`, `.yml`) are extracted.

3. Files are split into chunks. Each chunk is sent to the embedding service to generate a vector representation.

4. Chunks and embeddings are stored in PostgreSQL using the pgvector extension.

5. The API receives user queries, performs vector similarity search, and sends the retrieved context to the LLM.

## Tech Stack

Python 3.13 • FastAPI • SQLAlchemy • Alembic • PostgreSQL • pgvector • Sentence Transformers • PydanticAI • Ollama • Docker Compose

## Quick Start

```bash
cp .env.example .env
docker compose up
```
Run repositories index
```bash
docker compose run --rm indexer
```

The API will be available at:
http://localhost:8000/docs

## LLM Configuration

The project does not include an Ollama model. Ollama must be running separately and the API should be configured to connect to it through environment variables:
```
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
LLM_MODEL=qwen2.5-coder:7b
```
The model can be changed by updating LLM_MODEL to any compatible Ollama model.