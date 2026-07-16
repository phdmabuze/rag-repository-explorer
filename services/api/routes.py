from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.connection import get_session
from shared.db.models import Chunk
from shared.embeddings import embed_text

from .schemas import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
):
    query_embedding = embed_text(request.query)

    distance = Chunk.embedding.cosine_distance(query_embedding)

    stmt = (
        select(
            Chunk,
            distance.label("distance"),
        )
        .order_by(distance)
        .limit(5)
    )

    result = await session.execute(stmt)

    rows = result.all()

    return {
        "query": request.query,
        "chunks": [
            {
                "content": chunk.content,
                "source": chunk.source,
                "metadata": chunk.metadata_,
                "distance": distance,
            }
            for chunk, distance in rows
        ],
    }
