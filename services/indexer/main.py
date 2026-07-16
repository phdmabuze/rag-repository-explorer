import json

from .loader import iter_repository


def main():
    with open("sources.json", "r") as f:
        sources = json.load(f)

    print(f"Found {len(sources)} sources")
    for source in sources:
        for document in iter_repository(source["path"]):
            print(document.source)


if __name__ == "__main__":
    main()
