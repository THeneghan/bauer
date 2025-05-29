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


#
# def create_dataset_table_entry(session: Session, dataset_uuid: UUID, raw_file_name: str, gsutil_uri: str):
#     session.execute(
#         insert(DataSetID).values(dataset_uuid=str(dataset_uuid), raw_file_name=raw_file_name, gsutil_uri=gsutil_uri)
#     )
#     dataset_id = session.execute(select(DataSetID).where(DataSetID.dataset_uuid == str(dataset_uuid)))
#     return dataset_id
