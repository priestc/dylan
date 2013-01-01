import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from giotto.utils import better_base

Base = better_base()

from sqlite3 import dbapi2 as sqlite
engine = create_engine('sqlite+pysqlite:///file.db', module=sqlite)

session = sessionmaker(bind=engine)()
cache = None
auth_session = None

project_path = os.path.dirname(os.path.abspath(__file__))

from jinja2 import Environment, FileSystemLoader
jinja2_env = Environment(loader=FileSystemLoader(project_path + '/templates'))

debug = True
error_template = None

aws_access_key = 'AKIAJDBRZGUZ2PE334MQ'
aws_secret_access_key = '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'