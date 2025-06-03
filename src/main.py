from typing import List

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


def create_purchases_transaction(purchases: List[dict]) -> Purchases:
    purchase = purchases[0]
    return Purchases(
        external_id=purchase.get("external_id"),
        product_id=purchase.get("product_id"),
        time=purchase.get("time"),
        currency=purchase.get("currency"),
        price=purchase.get("price"),
        quantity=purchase.get("quantity"),
        properties=purchase.get("properties"),
    )


def create_events_transaction(events: List[dict]) -> Events:
    event = events[0]
    return Events(
        external_id=event.get("external_id"),
        properties=event.get("properties"),
        name=event.get("name"),
    )


if __name__ == "__main__":
    setup_logging()
    create_postgres_container(POSTGRES_CONTAINER_NAME, POSTGRES_PASSWORD=POSTGRES_PASSWORD, POSTGRES_USER=POSTGRES_USER)
    create_schema(engine)
    with open("../payloads.json") as f, Session() as session:
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
