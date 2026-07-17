from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.connection import get_session
from shared.db.models import Chunk
from shared.embeddings import embed_texts

from .llm import answer_question
from .schemas import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
):
    query_embedding = (await embed_texts([request.query]))[0]

    distance = Chunk.embedding.cosine_distance(query_embedding)

    stmt = (
        select(
            Chunk,
            distance.label("distance"),
        )
        .order_by(distance)
        .where(distance < 0.35)
        .limit(5)
    )

    result = await session.execute(stmt)

    rows = result.all()

    if not rows:
        return {
            "query": request.query,
            "answer": "I don't know",
            "chunks": [],
        }

    context = "\n\n".join(chunk.content for chunk, distance in rows)

    answer = await answer_question(
        request.query,
        context,
    )

    return {
        "query": request.query,
        "answer": answer,
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
