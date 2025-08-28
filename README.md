# 📚 Smart Librarian — RAG + Tool Calling

This project implements an AI librarian that recommends books using **OpenAI GPT + RAG (ChromaDB)**, then fetches a **detailed summary** via a **tool call**.

---

## Project Overview
Smart Librarian is an AI-powered book recommender. It uses OpenAI’s GPT models and a local vector database (ChromaDB) to suggest books based on your interests, and can fetch detailed summaries using a tool call.

---

## Folder structure
```
smart-librarian/
├─ app.py
├─ requirements.txt
├─ .env.example
├─ chroma/ 
├─ data/
│  ├─ book_summaries.md
│  └─ book_summaries_full.json
├─ rag/
│  ├─ ingest.py 
│  └─ retriever.py
├─ tools/
│  └─ summary_tool.py
└─ utils_openai_client.py
```

---

## File & Folder Explanations

- `app.py`: Handles user input, displays the UI, and interacts with the RAG retriever and summary tool to show book recommendations and summaries.
- `requirements.txt`: Lists all Python dependencies needed for the project (e.g., streamlit, openai, chromadb).
- `moderation.py`: Handles content moderation, filters inappropriate queries.
- `utils_openai_client.py`: Sets up the OpenAI API client using your API key. 
- `chroma/`: Contains the local ChromaDB database (`chroma.sqlite3`) where book summaries are stored as vector embeddings for semantic search.
- `data/`: 
   - `book_summaries.md`: Markdown file with short summaries of 20 books (used as RAG source).
   - `book_summaries_full.json`: JSON file with detailed book summaries (used for tool calls).
- `rag/`: 
   - `ingest.py`: Script to parse the markdown summaries and push them into ChromaDB.
   - `retriever.py`: Provides semantic search functionality to find relevant books based on user queries.
- `tools/`: 
   - `summary_tool.py`: Contains a function to fetch a detailed summary for a book by its title.
- `__pycache__/`: Stores Python bytecode cache files for faster loading (can be ignored).

---

## How-To-Run

1. Create and activate a virtual environment (Windows)
   
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies

   ```bash
   pip install -r requirements.txt
   pip install streamlit
   ```

3. Set up your OpenAI API key (temporary, for current session)
   
     ```bash
     $env:OPENAI_API_KEY="your-api-key-here"
     ```
5. Populate the vector store:
   ```powershell
   python rag/ingest.py
   ```
6. Run the Streamlit app:
   ```powershell
   streamlit run app.py
   ```
7. Open the local URL shown in the terminal to use the app.

---
