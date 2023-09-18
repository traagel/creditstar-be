from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

Session = scoped_session(sessionmaker())


# Create an engine bound to the app's configuration
def create_db_engine(app):
    user = app.config.get('PGUSER', '')
    password = app.config.get('PGPASSWORD', '')
    host = app.config.get('PGHOST', '')
    port = app.config.get('PGPORT')
    database = app.config.get('PGDATABASE', '')

    port_str = f":{port}" if port else ""

    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}{port_str}/{database}"
    )


def query_database(query, params=None):
    session = Session()
    try:
        results = session.execute(query, params).fetchall()
        return results
    finally:
        session.close()
        Session.remove()
