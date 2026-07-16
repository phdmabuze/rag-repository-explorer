import subprocess
from collections.abc import Iterator
from pathlib import Path

from .models import Document

EXTENSIONS = {".py", ".md", ".yaml", ".yml"}


def iter_repository(path: str) -> Iterator[Document]:
    files = subprocess.check_output(
        ["git", "-C", path, "ls-files"],
        text=True,
    ).splitlines()

    for file in files:
        file_path = Path(path) / file

        if file_path.suffix not in EXTENSIONS:
            continue

        yield Document(
            content=file_path.read_text(),
            source=str(file_path),
            metadata={
                "extension": file_path.suffix,
            },
        )
