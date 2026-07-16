import asyncio
import json

from sqlalchemy import delete

from shared.config import settings
from shared.db.connection import async_session
from shared.db.models import Chunk

from .chunker import chunk_document
from .embeddings import embed_chunk
from .loader import iter_repository


async def main():
    print("Indexing sources...")

    indexed_chunks = []

    with open("sources.json", "r") as f:
        sources = json.load(f)

    for source in sources:
        print(f"Indexing source: {source['url']}")

        for document in iter_repository(source["url"], source.get("branch", "main")):
            for chunk in chunk_document(
                document,
                settings.chunk_size,
                settings.chunk_overlap,
            ):
                indexed_chunks.append(embed_chunk(chunk))

    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Chunk))
            session.add_all(indexed_chunks)


if __name__ == "__main__":
    asyncio.run(main())
