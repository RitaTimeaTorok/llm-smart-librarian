import json, os

# Load the full summaries
DATA_PATH = os.path.join("data", "book_summaries_full.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    BOOKS = json.load(f)

# fetch a detailed summary for a given book title
def get_summary_by_title(title: str) -> str:
    return BOOKS.get(title, "Sorry, I don't have a full summary for that title yet.")
