"""DB integration tests - slightly messy approach to fixtures, would ideally refactor"""

from pathlib import Path

import docker
import ijson
from bauer_utils.db import create_postgres_sqlalchemy_engine
from bauer_utils.models import Attributes
from bauer_utils.sql_utils import check_external_id_exists
from main import create_events_transaction, create_purchases_transaction
from sqlalchemy import text
from sqlalchemy.orm import Session


def test_local_db(create_then_destroy_local_db, container_name):
    client = docker.from_env()
    assert container_name in [container.name for container in client.containers.list()]


def test_create_postgres_sqlalchemy_engine(
    create_then_destroy_local_db, pg_user, pg_password, local_host, db_name, port
):
    engine = create_postgres_sqlalchemy_engine(user=pg_user, password=pg_password, db_name=db_name, port=port)
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        collected_result = result.all()[0][0]
    assert collected_result == "hello world"


def test_smoke(
    create_then_destroy_local_db, pg_user, pg_password, local_host, db_name, port, create_then_destroy_tables
):
    """Effectively runs main"""
    engine = create_postgres_sqlalchemy_engine(user=pg_user, password=pg_password, db_name=db_name, port=port)
    bauer_path = Path(__file__).parent.parent
    json_file = bauer_path / "data/payloads.json"
    with open(json_file) as f, Session(engine) as session:
        for record in ijson.items(f, "item"):
            attributes = record["attributes"][0]
            events = record.get("events")
            purchase = record.get("purchases")
            attribute = Attributes(
                email=attributes.get("email"),
                external_id=attributes.get("external_id"),
            )
            if not check_external_id_exists(session, attributes.get("external_id")):
                session.add(attribute)
            if purchase:
                session.add(create_purchases_transaction(purchase))
            if events:
                session.add(create_events_transaction(events))
        session.commit()
