"""Reusable SQLalchemy utils"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from bauer_utils.models import Attributes, Base

POSTGRES_PASSWORD = "password"
POSTGRES_USER = "postgres"
engine = create_engine(f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/postgres", echo=False)
Session = sessionmaker(engine)


def create_schema(engine: Engine):
    Base.metadata.create_all(engine)  # Non-destructive so if table already exists nothing happens


def delete_tables(engine: Engine):
    Base.metadata.drop_all(bind=engine)


def check_external_id_exists(session: Session, external_id: int) -> bool:
    """Checks to see if this external id exists in the attributes table."""
    result = session.execute(select(Attributes).where(Attributes.external_id == external_id)).first() is not None
    return result
