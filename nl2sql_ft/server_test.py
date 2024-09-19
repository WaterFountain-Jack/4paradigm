import sys

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from loguru import logger
from nl2sql_hub.datasource import DataSource, get_url
from langchain.sql_database import SQLDatabase
from sentence_transformers import SentenceTransformer
import numpy as np
import subprocess
import time
import random
from utils_self.sql_prompt import (build_ft_sql_prompt,
                                   build_summary_prompt,
                                   build_cot_ft_sql_prompt)
import os
import uvicorn
import json
import openai
from openai import OpenAI
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings



app = FastAPI()
class SuccessResponse(BaseModel):
    success: bool



@app.post("/train_data")
# def tackle_train_data(request: TrainDataRequest):
async def tackle_train_data(request:Request):
    raw_data = await request.body()
   
    try:
        data_dict = json.loads(raw_data)
        print(data_dict)
        print(type(data_dict))
        print(data_dict['name'])
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
    return SuccessResponse(success=True)


if __name__ == "__main__":
    uvicorn.run("server_test:app", host="0.0.0.0", port=81)
