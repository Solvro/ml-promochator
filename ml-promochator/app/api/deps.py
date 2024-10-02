from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()

SessionDep = Annotated[Session, Depends(get_db)]
