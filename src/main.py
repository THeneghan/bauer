from typing import List
from sqlalchemy.sql.dml import Insert
import ijson
from bauer_utils.db import create_postgres_container
from bauer_utils.logging_utils import setup_logging
from bauer_utils.models import Attributes, Events, Purchases
from bauer_utils.sqlalchemy_utils import (
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    Session,
    check_external_id_exists,
    create_schema,
    engine,
)

POSTGRES_CONTAINER_NAME = "bauer_local_db"
BATCH_SIZE = 100


def create_purchases_transaction(purchases: List[dict]) -> Insert:
    purchase = purchases[0]
    return Purchases.__table__.insert().values(
        external_id=purchase.get("external_id"),
        product_id=purchase.get("product_id"),
        time=purchase.get("time"),
        currency=purchase.get("currency"),
        price=purchase.get("price"),
        quantity=purchase.get("quantity"),
        properties=purchase.get("properties"),
    )


def create_events_transaction(events: List[dict]) -> Insert:
    event = events[0]
    return Events.__table__.insert().values(
        external_id=event.get("external_id"),
        properties=event.get("properties"),
        name=event.get("name"),
    )


if __name__ == "__main__":
    setup_logging()
    create_postgres_container(POSTGRES_CONTAINER_NAME, POSTGRES_PASSWORD=POSTGRES_PASSWORD, POSTGRES_USER=POSTGRES_USER)
    create_schema(engine)
    with open("../payloads.json") as f:
        for record in ijson.items(f, "item"):
            attributes = record["attributes"][0]
            events = record.get("events")
            purchases = record.get("purchases")
            with Session() as session:
                attributes_transaction = Attributes.__table__.insert().values(
                    email=attributes.get("email"),
                    external_id=attributes.get("external_id"),
                )
                if not check_external_id_exists(session, attributes.get("external_id")):
                    session.execute(attributes_transaction)
                if purchases:
                    session.execute(create_purchases_transaction(purchases))
                if events:
                    session.execute(create_events_transaction(events))
                session.commit()
