import json

from shared.config import settings

from .chunker import chunk_document
from .embeddings import embed_chunk
from .loader import iter_repository


def main():
    print("Indexing sources...")

    with open("sources.json", "r") as f:
        sources = json.load(f)

    for source in sources:
        print(f"Indexing source: {source['path']}")
        for document in iter_repository(source["path"]):
            for chunk in chunk_document(
                document, settings.chunk_size, settings.chunk_overlap
            ):
                chunk = embed_chunk(chunk)


if __name__ == "__main__":
    main()
