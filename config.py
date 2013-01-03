import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from giotto.utils import better_base
from machine_config import *

Base = better_base()

from sqlite3 import dbapi2 as sqlite
engine = create_engine('sqlite+pysqlite:///file.db', module=sqlite)

session = sessionmaker(bind=engine)()

auth_session = None

project_path = os.path.dirname(os.path.abspath(__file__))

from jinja2 import Environment, FileSystemLoader
jinja2_env = Environment(loader=FileSystemLoader(project_path + '/templates'))

error_template = "error.html"