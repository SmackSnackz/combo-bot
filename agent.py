import requests
import json
from config import MODEL, anthropic_headers, anthropic_url
from doc_tools import search_documents
from db_tools import list_tables, describe_tables, run_query

TOOLS = [
    {
            "name": "search_documents",
            "description": "Search the user's notes for concepts and explanations. Not for facts about people, orders, or wallets.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search docs for answers."}
                },
                "required": ["query"],
            }
    }, 
    {
       "name": "list_tables",
       "description": "List the tables in the database. The database holds facts about people(name, age, city), their orders and their wallets.",
       "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "describe_tables",
        "description": "Show the column names and type of one table.",
        "input_schema": {
            "type": "object",
            "properties": {
                "table_name": {"type": "string", "description": "Name of the table"}
            },
            "required": ["table_name"],
        }


    },
    {
        "name": "run_query",
        "description": "Run a read only SQL SELECT query and return up to 50 rows as JSON. Use for facts about people, orders, and wallets, and for counting, totals, and filtering",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "A SELECT statement"}
            },
            "required": ["sql"],
        }
    }
]

TOOLS_FUNCTIONS = {
    "search_documents": search_documents,
    "list_tables": list_tables,
    "describe_tables": describe_tables,
    "run_query": run_query,
}


SYSTEM_PROMPT = (
    "You answer the questions using the user's notes and a database. "
    "Use search_documents for questions about concepts, definitions, and what the notes say. "
    "Use the database tools for questions about people, orders, wallets, or any counting, totals, or filtering. "
    "Inspect the schema before writing SQL. Never guess names, table names, or column names. "
    "If a tool returns nothing relevant, say so plainly. Never use outside knowledge. "
    "If a question mixes concepts and data about people, use search_documents for the concepts and the database tools for the people, then answer both. "
    "Before writing a query, call list_tables and describe_tables to see the real structure. "
    "If a query returns an error, read the error and try again. "
    "Answer only from tool results, and say plainly if the data does not contain the answer. "
    "Every question is about the user's own notes and database, never about the world in general. "
    "When you use search_documents, always say which file the answer came from, like (notes4.txt). "
    "Never ask permission to use a tool. Just use the tools and answer. "
    "You can not change data."
)



def run_agent(task, max_tokens=1024, max_steps=6):
    messages = [{"role": "user", "content": task}]
    steps_taken = []

    for _ in range(max_steps):
        body = {"model": MODEL, "max_tokens": max_tokens, "system": SYSTEM_PROMPT, "tools": TOOLS, "messages": messages}
        response = requests.post(anthropic_url, headers=anthropic_headers, json=body)
        data = response.json()
        if "content" not in data:
             return f"API error: {data}", steps_taken
        messages.append({"role": "assistant", "content": data["content"]})

        if data.get("stop_reason") != "tool_use":
            final_text = next((b["text"] for b in data["content"] if b["type"] == "text"), "")
            return final_text, steps_taken

        tool_results = []
        for block in data["content"]:
            if block["type"] == "tool_use":
                result = TOOLS_FUNCTIONS[block["name"]](**block["input"])
                steps_taken.append({"tool": block["name"], "input": block["input"]})
                tool_results.append({"type": "tool_result", "tool_use_id": block["id"], "content": result})
        messages.append({"role": "user", "content": tool_results})
        
    return "Agent stopped: hit max_steps without finishing.", steps_taken

if __name__ == "__main__":
    answer, steps = run_agent("What do my notes say about cosine similarity, and which people live in Dallas?")
    print(answer)
    print("\nSteps taken:")
    for s in steps:
        print(" -", s["tool"], s["input"])