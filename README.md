# COMBO-BOT

An AI agent that answers questions from two sources: my study notes and a SQLite database. It decides which one to use, or it uses both.

## What it does

- Searches my notes with RAG: the notes are chunked, embedded with Voyage, stored in Chroma, then reranked.
- Answers questions about people, orders, and wallets by read-only SQL queries (list tables, describe tables, run queries).
- Keeps conversation memory during a session, so follow-up questions work. It resets when you quit.

## Setup

1. Create a venv and run `pip install -r requirements.txt`.
2. Create a `.env` file with your own keys:
```
ANTHROPIC_API_KEY=your-key-here
VOYAGE_API_KEY=your-key-here
```

3. Build the database and search index, then start the chat:

```
python setup_db.py
python ingest.py
python main.py
```

## Files

- `main.py`: terminal chat.
- `agent.py`: the tool menu, the system prompt, and the loop that lets Claude choose tools.
- `db_tools.py`: the database tools (list tables, describe tables, run query).
- `doc_tools.py`: the `search_documents` tool.
- `embeddings.py`: embeds and reranks text with Voyage.
- `chunking.py`: splits documents into pieces.
- `ingest.py`: loads the notes, embeds them, and stores them.
- `vector_store.py`: opens the Chroma vector database
- `schema.sql` and `seed.sql`: the database structure and its data.
- `setup_db.py`: builds `combobot.db` from the two SQL files.
- `config.py`: keys, model names, URLs, and headers.
- `test_agent.py`: the evaluation tests.

## Safety

- Read-only database connection.
- SELECT-only queries.
- A 50-row cap on results

## Tests

```
python test_agent.py
```

14 tests, including an off-topic refusal and a delete trap.