Here’s why it qualifies as an **SQL Agent** and how it works:

1️.Accepts **natural language input** (e.g., *“Show all employees in the sales department”*).

2️.Converts it into a valid **SQL query** using Groq’s LLM (via LangChain).

3️.Dynamically **fetches table schema** (columns & types) from MySQL for accurate SQL generation.

4️.Injects this schema into the **LLM prompt** for context-aware queries.

5️.Differentiates between raw SQL and NL input, handling both seamlessly.

6️.Executes **SELECT, INSERT, UPDATE, DELETE** on the database.

7️.Cleans up LLM output by removing markdown/code artifacts like \`\`\`sql.

8️.Exposes everything through a **FastAPI endpoint**, making it easy for clients to query via API.

#How to run locally
cd sql-agent
pip install -r requirements.txt
# (optional) set env vars or create .env
pip show uvicorn
pip install uvicorn[standard]
pip install fastapi uvicorn psycopg2-binary
pip install openai langchain langchain-community

to start interactive shell
python sql_shell.py
Run the client script in another terminal:python client.py
pip install langchain langchain-openai
pip install python-dotenv
https://console.groq.com/home[APIKEY]

uvicorn app:app --reload --port 8000
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT NOW() as ts;"}'
Build & “publish” with Docker
# from the sql-agent folder
docker build -t sql-agent:latest .
docker run --rm -p 8000:8000 \
  -e PG_HOST=host.docker.internal \
  -e PG_PORT=5432 \
  -e PG_DB=postgres \
  -e PG_USER=postgres \
  -e PG_PASS=postgres \
  sql-agent:latest

http://localhost:8000

curl -X POST http://localhost:8000/sqlagent \
  curl -X 'POST' \
  'http://127.0.0.1:8000/sqlagent' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sql": "change email to jayaai7650@gmail.com all fields fields of employee "
}


How to get token: https://console.groq.com/home
just signup and get details.


curl -X 'POST' \
  'http://127.0.0.1:8000/sqlagent' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sql": "add  data to  managers table  id 100216, manager_name  jaya"
}'

Response body
Download
{
  "query": "INSERT INTO employee (EmpID, FirstName, LastName, Email, PhoneNumber, HireDate, JobTitle, Salary, DepartmentID) \nVALUES (100216, 'Jaya', NULL, NULL, NULL, NULL, 'Manager', NULL, NULL);",
  "rows": [
    {
      "status": "success",
      "affected_rows": 1
    }
  ]
}

About Me
I’m Jayakrishna M, an IT professional with 10+ years of experience. I began my career in Java & Spring Boot and have since expanded into Python, LLMs, AI Agents, NumPy, and Pandas. Recently, I built my first SQL Agent project.

📩 Feel free to reach out: mjk7650@gmail.com


