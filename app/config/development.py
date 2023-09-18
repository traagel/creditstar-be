import os

DATABASE_URL = os.getenv("DEV_DATABASE_URL")
PGPASSWORD = os.getenv("PGPASSWORD")
PGHOST = os.getenv("PGHOST")
PGUSER = os.getenv("PGUSER")
PGDATABASE = os.getenv("PGDATABASE")
PGPORT = os.getenv("PGPORT")
VERSION = os.getenv("VERSION")

DEBUG = False
