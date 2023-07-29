import h11
import os
import time
import json
import ast
import uvicorn
import traceback
import zipfile
import threading
import datetime
import configparser
from typing import List
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request, Depends, File
from fastapi.responses import ORJSONResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from core.celery_app import celery_app
from utils import celery_util, time_util

import schemas
import db_crud
from model import article, newspaper
from database import SessionLocal, engine
from pprint import pprint

#FastAPI setup
config = configparser.ConfigParser()
config.read('config.ini')
title="News Crawling Service"
app = FastAPI(title=title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

newspaper.Base.metadata.create_all(bind=engine)
article.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_v2():
    return SessionLocal()

@app.post("/api/v1/newspaper/add")
def create_newspaper_site(newspaper_site: schemas.NewspaperSite, db=Depends(get_db)):
    try:
        return db_crud.create_newspaper_site(db=db, newspaper_site=newspaper_site)
    except Exception as e:
        logger.info(f"Error: {e} when adding newspaper site {newspaper_site.source_url} ")
        return {"error": f"Error: {e} when adding newspaper site {newspaper_site.source_url} "}

@app.delete("/api/v1/article/delete_all")
def delete_all_articles(db=Depends(get_db)):
    db_crud.delete_all_articles(db=db)
    return schemas.ResponseBase(message="Deleted all articles")


    

