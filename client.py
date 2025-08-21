# client.py
import requests

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


if __name__ == "__main__":
    # Example 1: simple select
    result = run_query("SELECT * FROM your_table")
    print("Result:", result)

    # Example 2: with params
    result = run_query(
        "SELECT * FROM your_table WHERE id = %(id)s",
        params={"id": 1}
    )
    print("Result with params:", result)

    # Example 3: explain plan
    result = run_query("SELECT * FROM your_table WHERE id < 10", explain=True)
    print("Explain plan:", result)
