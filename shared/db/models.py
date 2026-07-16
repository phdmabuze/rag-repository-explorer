import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )

    content: Mapped[str] = mapped_column(Text)

    source: Mapped[str]

    metadata_: Mapped[dict] = mapped_column(JSONB)

    embedding: Mapped[list[float]] = mapped_column(Vector(384))
