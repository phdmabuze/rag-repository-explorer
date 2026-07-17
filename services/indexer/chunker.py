from collections.abc import Iterator

from .schemas import Document


def chunk_document(
    document: Document, chunk_size: int, chunk_overlap: int
) -> Iterator[dict]:
    text = document.content

    start = 0

    while start < len(text):
        end = start + chunk_size

        yield dict(
            content=text[start:end],
            source=document.source,
            metadata={
                **document.metadata,
                "chunk_start": start,
                "chunk_end": end,
            },
        )

        start += chunk_size - chunk_overlap
