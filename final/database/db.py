from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()
SQL_URL = os.environ.get("SQL_URL")

engine = create_engine(SQL_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)