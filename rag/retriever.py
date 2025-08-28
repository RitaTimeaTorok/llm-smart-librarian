import os
import chromadb
from chromadb.utils import embedding_functions

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma")

_client = None
_coll = None


def _initialize_collection():
    global _client, _coll
    if _coll is not None:
        return _coll
    _client = chromadb.PersistentClient(path=PERSIST_DIR)
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    _coll = _client.get_or_create_collection(name="book_summaries", embedding_function=embedding_function)
    return _coll


def search(query: str, k: int = 3):
    coll = _initialize_collection()
    res = coll.query(query_texts=[query], n_results=k, include=["documents", "metadatas", "distances"])
    # print(f"Retriever debug: {len(res['documents'][0])} results returned for query '{query}'")
    results = []

    for i in range(len(res["documents"][0])):
        doc = res["documents"][0][i]
        meta = res["metadatas"][0][i]
        dist = res["distances"][0][i]

        # Parse title and author from metadata
        title = meta.get("title", "Unknown Title")
        author = meta.get("author", "Unknown Author")
        results.append({"title": title, "author": author, "document": doc, "metadata": meta, "distance": float(dist)})

    return results
