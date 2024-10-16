from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import psycopg2
import os
from contextlib import asynccontextmanager



connection = psycopg2.connect(
            database="fastapi", 
            user='postgres',
            password='password',
            host='127.0.0.1',
            port='5434',
        )
cursor = connection.cursor()

postgres_insert_query = """ INSERT INTO tasks (id, name, description)
                                       VALUES (%s,%s,%s)"""

postgres_select_query = """ SELECT * FROM tasks"""




app = FastAPI(title="TO DO LIST")

class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


tasks = []

@app.post("/add_task")
async def add_task(task:Annotated[STaskAdd, Depends()],):
    task_add = (task.id, task.name, task.description)
    cursor.execute(postgres_insert_query, task_add)
    connection.commit()
    tasks.append(task)
    return {"ok":True}

@app.get("/get_task")
async def get_task():
    cursor.execute(postgres_select_query)
    tasks = cursor.fetchall()
    return {"ok":True, "task": tasks}

@app.delete("delete_task")
async def delete_task(id):
    postgres_delete_query = f"DELETE FROM tasks WHERE id = '{id}'"
    cursor.execute(postgres_delete_query)
    connection.commit()
    return {"ok":True, "id": id}

