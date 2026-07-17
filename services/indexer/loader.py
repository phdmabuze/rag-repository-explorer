import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import urlparse

from .models import Document

EXTENSIONS = {".py", ".md", ".yaml", ".yml"}


def github_file_url(url: str, branch: str, file: str) -> str:
    parsed = urlparse(url)

    path_parts = parsed.path.rstrip("/").removesuffix(".git")

    return f"https://github.com{path_parts}/blob/{branch}/{file}"


def iter_repository(url: str, branch: str = "main") -> Iterator[Document]:
    path = Path(tempfile.mkdtemp())

    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            branch,
            url,
            str(path),
        ],
        check=True,
    )

    files = subprocess.check_output(
        ["git", "-C", path, "ls-files"],
        text=True,
    ).splitlines()

    for file in files:
        file_path = path / file

        if file_path.suffix not in EXTENSIONS:
            continue

        yield Document(
            content=file_path.read_text(),
            source=github_file_url(url, branch, file),
            metadata={
                "extension": file_path.suffix,
                "path": file,
            },
        )
