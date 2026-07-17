import httpx

from shared.config import settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.embedding_service_url}/embed",
            json={"texts": texts},
        )

    response.raise_for_status()

    return response.json()["embeddings"]
