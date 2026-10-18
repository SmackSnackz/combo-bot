import sqlite3
import json

def list_tables():
    conn = sqlite3.connect("file:combobot.db?mode=ro", uri=True)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cursor.fetchall()
    conn.close()
    return ", ".join(row[0] for row in rows)

def describe_tables(table_name):
    """Describe the columns of a table using PRAGMA table_info.
    Steps:
    1. Get real table names
    2. Validate the requested name
    3. Connect read-only
    4. Run PRAGMA table_info(table_name)
    5. Fetch and close
    6. return column names as text
    """

    # 1. get the real table names
    valid = list_tables().split(", ")

    # 2. validate
    if table_name not in valid:
        return f"Unknown table: {table_name}. Valid tables: {', '.join(valid)}"

    # 3. connect read-only
    conn = sqlite3.connect("file:combobot.db?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 4. PRAGMA table_info
    cursor.execute(f"PRAGMA table_info({table_name})")

    # 5. fetch and close
    columns = cursor.fetchall()
    conn.close()
    if not columns:
        return f"Table '{table_name}' has no columns."

    lines = []
    for col in columns:
        lines.append(f"{col['name']} ({col['type']})")

    return "\n".join(lines)

def run_query(sql):
    """Run a read-only SELECT and return the rows as JSON text."""
    cleaned = sql.strip()

    if not cleaned.upper().startswith("SELECT"):
        return "Only SELECT queries are allowed." 

    conn = sqlite3.connect("file:combobot.db?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(cleaned)
        rows = cursor.fetchmany(50)
    except Exception as e:
        return f"Query error: {e}"
    finally:
        conn.close()

    return json.dumps([dict(row) for row in rows])

# 5. Test lines
# #----- -----------------------------
if __name__ == "__main__":
    print("Tables:", list_tables())
    print()

    print("Describe 'people':")    
    print(describe_tables("people"))
    print()

    print("Describe 'wallets':")
    print(describe_tables("wallets"))
    print()

    print("Describe 'orders':")
    print(describe_tables("orders"))
    print()

    print("Run query:")
    result = run_query("SELECT * FROM people LIMIT 50;")
    print(result)
    print(run_query("DELETE FROM people")) 
    print(run_query("SELECT * FROM nothing"))





    