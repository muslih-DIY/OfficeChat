from typing import Optional

from sqlmodel import Field, SQLModel, create_engine,Session


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

# Dependency
async def get_db_Session():
    with Session(engine) as session:
        yield session


def create_all_table():
       
    SQLModel.metadata.create_all(engine)

