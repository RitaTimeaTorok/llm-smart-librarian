import os, re, uuid
import chromadb
from chromadb.utils import embedding_functions

# Read the location where ChromaDB will store data
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma")


def extract_book_information(path: str):
    # Read book_summaries.md
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split on '## Title:' headers
    parts = re.split(r"^##\s*Title:\s*", text, flags=re.MULTILINE)

    # Hold all the book items, extract title, author, and summary
    items = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.splitlines()
        title = lines[0].strip()
        author = "Unknown Author"
        summary_lines = []
        for line in lines[1:]:
            if line.strip().startswith("**Author:**"):
                author = line.strip().replace("**Author:**", "").strip()
            else:
                summary_lines.append(line)
        summary = "\n".join(summary_lines).strip()
        items.append((title, author, summary))

    return items


def main():
    book_summaries_file_path = os.path.join("data", "book_summaries.md")
    items = extract_book_information(book_summaries_file_path)

    # Setup ChromaDB + Embeddings
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    coll = client.get_or_create_collection(name="book_summaries", embedding_function=embedding_function)

    ids, docs, metas = [], [], []
    for title, author, summary in items:
        ids.append(str(uuid.uuid4()))
        docs.append(f"Title: {title}\nAuthor: {author}\n{summary}")
        metas.append({"title": title, "author": author})

    # Insert/update in ChromaDB
    if ids:
        coll.upsert(ids=ids, documents=docs, metadatas=metas)

    print(f"Ingested {len(ids)} items into collection 'book_summaries' at {PERSIST_DIR}")


if __name__ == "__main__":
    main()
