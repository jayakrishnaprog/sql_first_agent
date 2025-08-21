About Me
I’m Jayakrishna Mudimanchi, an IT professional with 10+ years of experience. I began my career in Java & Spring Boot and have since expanded into Python, LLMs, AI Agents, NumPy, and Pandas. Recently, I built my first SQL Agent project.

📩 Feel free to reach out: jayaai7650@gmail.com

#How run locally
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
