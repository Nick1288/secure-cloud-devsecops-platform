from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

class UserCreate(BaseModel):
    name: str

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def get_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users ORDER BY id;")
            rows = cur.fetchall()

    return [
        {"id": row[0], "name": row[1]}
        for row in rows
    ]


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name) VALUES (%s) RETURNING id, name;",
                (user.name,)
            )
            new_user = cur.fetchone()

    return {
        "id": new_user[0],
        "name": new_user[1]
    }