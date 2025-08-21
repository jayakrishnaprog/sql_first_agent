# sql_shell.py
import requests
import json

API_URL = "http://127.0.0.1:8000/query"

def run_query(sql: str, params: dict = None, explain: bool = False, limit: int = 1000):
    payload = {
        "sql": sql,
        "params": params,
        "limit": limit,
        "explain": explain
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None


def interactive_shell():
    print("🟢 Welcome to SQL Agent Shell (connected to http://127.0.0.1:8000)")
    print("Type SQL queries directly. Commands:")
    print("   :q        -> quit")
    print("   :explain  -> toggle explain mode ON/OFF")
    print("   :limit n  -> set row limit (default 1000)")
    print("----------------------------------------------------")

    explain_mode = False
    row_limit = 1000

    while True:
        sql = input("SQL> ").strip()
        if not sql:
            continue

        if sql.lower() in {":q", "quit", "exit"}:
            print("👋 Exiting SQL Agent Shell.")
            break

        if sql.lower() == ":explain":
            explain_mode = not explain_mode
            print(f"🔎 Explain mode: {'ON' if explain_mode else 'OFF'}")
            continue

        if sql.lower().startswith(":limit"):
            try:
                row_limit = int(sql.split()[1])
                print(f"📊 Row limit set to {row_limit}")
            except Exception:
                print("⚠️ Usage: :limit <number>")
            continue

        # Run query
        result = run_query(sql, explain=explain_mode, limit=row_limit)
        if result:
            print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    interactive_shell()
