from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()
SQL_URL = os.environ.get("SQL_URL")


# create the engine
engine = create_engine(SQL_URL, echo=True)

SQLModel.metadata.create_all(engine)