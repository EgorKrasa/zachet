from flask import Flask
import psycopg2, os

app = Flask(__name__)

def q(sql, params=None, fetch=False):
    with psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None

@app.route("/create/<title>")
def create(title):
    q("INSERT INTO tasks (title) VALUES (%s)", (title,))
    return "created"

@app.route("/done/<int:id>")
def done(id):
    q("UPDATE tasks SET done = TRUE WHERE id = %s", (id,))
    return "updated"

@app.route("/pending")
def pending():
    rows = q("SELECT id, title FROM tasks WHERE done = FALSE", fetch=True)
    return "\n".join(f"{r[0]} {r[1]}" for r in rows) or "no pending tasks"

@app.route("/stats")
def stats():
    total = q("SELECT COUNT(*) FROM tasks", fetch=True)[0][0]
    done = q("SELECT COUNT(*) FROM tasks WHERE done = TRUE", fetch=True)[0][0]
    return f"total: {total} done: {done} pending: {total-done}"

@app.route("/")
def home():
    return "Todo API running"

if name == "__main__":
    app.run(host="0.0.0.0", port=5000)