from langchain.tools import tool

import db_tools
from doc_tools import search_documents as _search_documents


@tool
def search_documents(query: str) -> str:
    """Search the user's notes for concepts and explinations. Not for facts about people, orders, or wallets."""
    return _search_documents(query)

@tool
def list_tables() -> str:
    """List the tables in the database. The database holds facts about people(name, city, age), their orders, and their wallets."""
    return db_tools.list_tables()

@tool
def describe_tables(table_name: str) -> str:
    """Show the column names and types of one table."""
    return db_tools.describe_tables(table_name)

@tool
def run_query(sql: str) -> str:
    """Run a read-only SQL SELECT query and return up tp 50 rows as JSON. Use for facts about people, orders, and wallets, and for counting, totals, and filtering."""
    return db_tools.run_query(sql)