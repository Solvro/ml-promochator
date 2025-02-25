from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session
import dotenv
import os

dotenv.load_dotenv()

postgres_url = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"

engine = create_engine(postgres_url)


def get_session():
    """
    Dependency function that provides a database session.

    This function creates a new session using the SQLModel engine and yields it.
    The session is automatically closed when the request is completed.

    Yields:
        Session: A database session.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
