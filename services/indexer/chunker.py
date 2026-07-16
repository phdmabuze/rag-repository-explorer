from collections.abc import Iterator

from shared.config import settings

from .models import Chunk, Document


def chunk_document(
    document: Document, chunk_size: int, chunk_overlap: int
) -> Iterator[Chunk]:
    text = document.content

    start = 0

    while start < len(text):
        end = start + settings.chunk_size

        yield Chunk(
            content=text[start:end],
            source=document.source,
            metadata={
                **document.metadata,
                "chunk_start": start,
                "chunk_end": end,
            },
        )

        start += settings.chunk_size - settings.chunk_overlap
