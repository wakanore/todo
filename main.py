from datetime import datetime
from enum import Enum
from typing import List, Optional, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import psycopg2
import os
from contextlib import asynccontextmanager



connection = psycopg2.connect(
            database="fastapi",  # эта БД уже должна быть
            user='postgres',
            password='5678',
            host='127.0.0.1',
            port='5434',
        )
cursor = connection.cursor()

postgres_insert_query = """ INSERT INTO tasks (id, name, description)
                                       VALUES (%s,%s,%s)"""

postgres_select_query = """ SELECT * FROM tasks"""

postgres_delete_query = """ DELETE FROM tasks WHERE id = '{id}'"""



app = FastAPI(title="Trading App")

class STaskAdd(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


tasks = []

@app.post("/tasks")
async def add_task(task:Annotated[STaskAdd, Depends()],):
    task_add = (task.id, task.name, task.description)
    cursor.execute(postgres_insert_query, task_add)
    connection.commit()
    tasks.append(task)
    return {"ok":True}
