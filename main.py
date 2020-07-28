from sqlalchemy import create_engine
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://username:password@localhost:3306/codex_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Postgresql@127.0.0.1:5432/postgres"

# # db = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# conn = engine.connect()
if(engine.connect()):
    conn = engine.connect()
    print('Database connected')
else:
    print('Database not connected')

app = FastAPI(title="REST API using FastAPI MYSQL Async EndPoints by Cobby")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    name: str
    age: int
    gender: str


class Codex(BaseModel):
    id: Optional[int] = None
    code: str
    description: str


@app.get("/get-all-codex")
def get_all_codex():
    name = "Frank"
    query = conn.execute(
        "SELECT * FROM code_desc")
    data = query.fetchall()
    return {"responseCode":  "00", "message": "Students fetched successfully", "data": data}


@app.post("/create-codex")
async def create_codex(codex: Codex):
    query = "INSERT INTO code_desc(code, description) VALUES(%s, %s)"
    if(conn.execute(query, (codex.code, codex.description))):
        return {"responseCode":  "00", "message": "Students fetched successfully", "data": codex}
    else:
        return {"responseCode":  "500", "message": "Failed to insert", "data": None}


@app.put("/modify-codex/{codex_id}")
async def modify_codex(codex_id: int, codex: Codex):
    query_check = conn.execute(
        "SELECT * FROM code_desc WHERE id = %s ", (codex_id))
    data = query_check.fetchone()
    if data.id == codex_id:
        query = "UPDATE code_desc SET  code = %s, description = %s WHERE id = %s"
        if(conn.execute(query, (codex.code, codex.description, codex_id))):
            resp = {"id": codex_id, "code": codex.code,
                    "description": codex.description}
            return {"responseCode":  "00", "message": "Codex fetched successfully", "data": resp}
        else:
            return {"responseCode":  "500", "message": "Failed to update", "data": None}
    else:
        return {"responseCode":  "404", "message": "No data found", "data": None}


@app.delete("/delete-codex/{codex_id}")
async def delete_codex(codex_id: int):
    query_check = conn.execute(
        "SELECT * FROM code_desc WHERE id = %s ", (codex_id))
    if query_check:
        data = query_check.fetchone()
        if None == data:
            resp = {"responseCode":  "404",
                    "message": "No data found", "data": None}
            raise HTTPException(status_code=404, detail=resp)
            # return {"responseCode":  "404", "message": "No data found", "data": None}
        print(data.id)
        if data.id == codex_id:
            query_delete = conn.execute(
                "DELETE FROM code_desc WHERE id = %s ", (codex_id))

            if query_delete:
                resp = {"codex_id": codex_id}
                return {"responseCode":  "00", "message": "Codex deleted successfully", "data": resp}
            else:
                return {"responseCode":  "500", "message": "Failed to delete codex", "data": None}
        else:
            return {"responseCode":  "404", "message": "No data found", "data": None}
    else:
        return {"responseCode":  "404", "message": "No data found", "data": None}
