from sentence_transformers import SentenceTransformer

from .models import Chunk

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def embed_chunk(chunk: Chunk) -> Chunk:
    vector = model.encode(chunk.content)

    chunk.metadata["embedding"] = vector.tolist()

    return chunk
