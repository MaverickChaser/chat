import sys
import os

print(sys.path)
print(__name__)

from common.models_db import Base
from database.config import dbUrlBase, dbName, defaultConnectArgs
from sqlalchemy import create_engine

engine = create_engine(dbUrlBase, connect_args = defaultConnectArgs, encoding = 'utf-8', echo = True)
engine.execute("CREATE DATABASE IF NOT EXISTS " + dbName)
engine.execute("USE " + dbName)
Base.metadata.create_all(engine)
