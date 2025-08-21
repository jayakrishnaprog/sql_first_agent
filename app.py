import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import mysql.connector
from mysql.connector import pooling, Error

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

# ---------- Load env ----------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------- LLM ----------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)

# ---------- DB Config ----------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "jaya")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "tiger")

mysql_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

# ---------- FastAPI ----------
app = FastAPI(title="MySQL SQL Agent (Groq)", version="1.0")

class QueryRequest(BaseModel):
    sql: str   # can be SQL or natural language

class QueryResponse(BaseModel):
    query: str
    rows: Optional[List[Dict[str, Any]]] = None


# ---------- Schema Reader ----------
def get_table_schema(table_name: str) -> str:
    """Fetch column names and types from MySQL table"""
    try:
        conn = mysql_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        schema_str = ", ".join([f"{col[0]} ({col[1]})" for col in columns])
        return schema_str
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Schema fetch error: {str(e)}")


# ---------- AI Agent ----------
def build_prompt(nl_query: str, table_name: str) -> str:
    schema = get_table_schema(table_name)
    sql_prompt = PromptTemplate(
        input_variables=["question", "schema"],
        template="""
You are an expert SQL generator. Convert the following natural language request into a valid MySQL query.

The table is `{table}` with schema:
{schema}

Rules:
- Only use the fields explicitly mentioned in the request.
- For other fields in INSERT or UPDATE, let MySQL use DEFAULT values (auto_increment, NULL, or defined defaults).
- Always generate valid MySQL syntax.
- Return ONLY the SQL query, no explanations, no markdown.

Question: {question}
SQL:
"""
    )
    chain = LLMChain(llm=llm, prompt=sql_prompt)
    response = chain.invoke({"question": nl_query, "schema": schema, "table": table_name})
    sql = response["text"].strip()
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("```", "").strip()
    return sql


# ---------- Endpoint ----------
@app.post("/sqlagent", response_model=QueryResponse)
def run_query(payload: QueryRequest = Body(...)):
    user_input = payload.sql.strip()
    table_name = "employee"  # can make dynamic later

    if not user_input.lower().startswith(("select", "insert", "update", "delete")):
        generated_sql = build_prompt(user_input, table_name)
    else:
        generated_sql = user_input

    try:
        conn = mysql_pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(generated_sql)

        if generated_sql.lower().startswith("select"):
            rows = cursor.fetchall()
        else:
            conn.commit()
            rows = [{"status": "success", "affected_rows": cursor.rowcount}]

        cursor.close()
        conn.close()

        return QueryResponse(query=generated_sql, rows=rows)

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
