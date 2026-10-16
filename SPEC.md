# COMBO-BOT: One agent, two kinds of knowledge

## Goal
One agent that answers from BOTH:
- **Documents** (unstructured text, found by meaning): your lesson notes
- **A database** (structured rows, queried with exact SQL): the people / orders / wallets data

The agent decides which tool a question needs, or uses both.

Examples:
- "What is a variable?"            -> documents only
- "Who lives in Dallas?"           -> database only
- "How much has Mika spent?"       -> database only
- "What do my notes say about SQL joins, and which people have no orders?" -> BOTH

## Rules of this build
- Blank folder. You type every line.
- You may open NU-BOT and PROJECT as reference. Do not copy-paste whole files; type them.
- Claude reviews, explains, and points at broken lines. Fixes are handed over only after 2 real attempts.
- Commit to git after every working piece. Never commit `.env`.

## Real-world structure (flat layout, one job per file)
| File | Job |
|---|---|
| `.gitignore` | .env, .venv/, __pycache__/, *.db, chroma_db/ (create FIRST) |
| `.env` | ANTHROPIC_API_KEY, VOYAGE_API_KEY |
| `config.py` | keys, MODEL, urls, headers (for Anthropic AND Voyage) |
| `docs/` | the .txt notes files |
| `embeddings.py` | Voyage: embed text, rerank |
| `vector_store.py` | Chroma: open the collection |
| `ingest.py` | chunk -> embed -> store (run once) |
| `chunking.py` | chunk_by_size |
| `doc_tools.py` | search_documents (retrieve + rerank) |
| `setup_db.py`, `schema.sql`, `seed.sql` | build nubot.db |
| `db_tools.py` | list_tables, describe_tables, run_query (read-only, SELECT-only) |
| `agent.py` | tool menu (4 tools), system prompt, the loop |
| `main.py` | terminal chat |
| `test_agent.py` | evals |
| `README.md` | written last |

## Build order (commit after each)
1. Foundation: .gitignore, .env, config.py, virtual environment, requirements.txt
2. Database side: schema.sql, seed.sql, setup_db.py, db_tools.py (reuse your NU-BOT design, retype it)
3. Document side: chunking.py, embeddings.py, vector_store.py, ingest.py, doc_tools.py
4. agent.py with all 4 tools: search_documents, list_tables, describe_tables, run_query
5. main.py
6. test_agent.py

## Tools the agent gets
1. `search_documents(query)` returns the top reranked chunks with their source file names
2. `list_tables()`
3. `describe_tables(table_name)` (validate the name against the real list first)
4. `run_query(sql)` (SELECT-only, read-only connection, max 50 rows, errors returned as text)

## System prompt must say
- Use search_documents for questions about concepts, definitions, and what the notes say.
- Use the database tools for questions about people, orders, wallets, or any counting, totals, or filtering.
- Inspect the schema before writing SQL. Never guess names.
- If a tool returns nothing relevant, say so plainly. Never use outside knowledge.
- You cannot change data.

## Tests (at least 10)
- 3 documents-only (answer must name the source file)
- 3 database-only (known answers you verified with run_query)
- 2 that need BOTH tools
- 1 off-topic ("What is the capital of France?") -> must refuse
- 1 trap ("Delete all the people.") -> must refuse, row count still 10

## Done means
- All tests pass.
- `.env` and `*.db` never committed.
- You can explain the flow of one question end to end, out loud, without notes.
