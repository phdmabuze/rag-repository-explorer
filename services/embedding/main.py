from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from sentence_transformers import SentenceTransformer

from .schemas import EmbedRequest, EmbedResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading embedding model...")

    app.state.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    print("Embedding model loaded")

    yield

    print("Shutting down embedding service")


app = FastAPI(lifespan=lifespan)


@app.post("/embed", response_model=EmbedResponse)
async def embed(request: EmbedRequest) -> EmbedResponse:
    model: SentenceTransformer = app.state.model

    embeddings = await run_in_threadpool(
        model.encode,
        request.texts,
        convert_to_numpy=True,
    )

    return EmbedResponse(
        embeddings=embeddings.tolist(),
    )
