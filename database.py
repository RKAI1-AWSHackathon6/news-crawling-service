from requests import Session 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# A simple db for now
# get db
def get_id_db(txt_path):
    db = []
    with open(txt_path, 'r') as f:
        for line in f:
            db.append(line.strip())
    return db  

class SimpleDB:
    MAX_RETURN_DB = 100
    def __init__(self,txt_path):
        self.db = get_id_db(txt_path)        
        self.current_id_index = 0
    
    def get_ids(self):
        # Get ids from db
        if self.current_id_index < len(self.db):
            end_idx = min(self.current_id_index+SimpleDB.MAX_RETURN_DB,len(self.db))
            data = self.db[self.current_id_index:end_idx]
            self.current_id_index += SimpleDB.MAX_RETURN_DB
            return data
        else:
            return []



SQLALCHEMY_DATABASE_URL = "sqlite:///database/collection.db"

# engine = create_engine(
#     settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()