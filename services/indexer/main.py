import asyncio
import json

from sqlalchemy import delete

from shared.config import settings
from shared.db.connection import async_session
from shared.db.models import Chunk
from shared.embeddings import embed_texts

from .chunker import chunk_document
from .loader import iter_repository


async def main():
    print("Indexing sources...")

    with open("sources.json", "r") as f:
        sources = json.load(f)

    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Chunk))

    for source in sources:
        print(f"Indexing source: {source['url']}")

        try:
            chunks = []

            for document in iter_repository(
                source["url"],
                source.get("branch", "main"),
            ):
                chunks.extend(
                    chunk_document(
                        document,
                        settings.chunk_size,
                        settings.chunk_overlap,
                    )
                )

            if not chunks:
                print("No chunks found, skipping")
                continue

            print(f"Created {len(chunks)} chunks")

            embeddings = await embed_texts([chunk["content"] for chunk in chunks])

            db_chunks = [
                Chunk(
                    content=chunk["content"],
                    source=chunk["source"],
                    metadata_=chunk["metadata"],
                    embedding=embedding,
                )
                for chunk, embedding in zip(
                    chunks,
                    embeddings,
                    strict=True,
                )
            ]

            async with async_session() as session:
                async with session.begin():
                    session.add_all(db_chunks)

            print(f"Saved {len(db_chunks)} chunks")

        except Exception as e:
            print(f"Failed to index {source['url']}: {e}")
            continue

    print("Indexing finished")


if __name__ == "__main__":
    asyncio.run(main())
