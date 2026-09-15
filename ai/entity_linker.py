import re
from graph.database import Neo4jDatabase


def normalize(value: str):
    return " ".join(value.lower().strip().split())


def find_person(name: str):
    db = Neo4jDatabase()

    query = """
    MATCH (p:Person)
    WHERE toLower(p.name) = toLower($name)
    RETURN p.id AS id, p.name AS name
    LIMIT 1
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(query, name=name)
        record = result.single()

    db.close()

    if record is None:
        return None

    return {
        "id": record["id"],
        "name": record["name"]
    }


def find_vehicle(registration: str):
    db = Neo4jDatabase()

    query = """
    MATCH (v:Vehicle)
    WHERE toLower(v.registration) = toLower($registration)
    RETURN v.id AS id, v.registration AS registration
    LIMIT 1
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(
            query,
            registration=registration
        )
        record = result.single()

    db.close()

    if record is None:
        return None

    return {
        "id": record["id"],
        "registration": record["registration"]
    }


def find_phone(number: str):
    db = Neo4jDatabase()

    query = """
    MATCH (p:Phone)
    WHERE p.number = $number
    RETURN p.id AS id, p.number AS number
    LIMIT 1
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(
            query,
            number=number
        )
        record = result.single()

    db.close()

    if record is None:
        return None

    return {
        "id": record["id"],
        "number": record["number"]
    }


def link_entity(entity: dict):
    entity_type = entity["label"]
    text = entity["text"]

    if entity_type == "PERSON":
        match = find_person(text)

    elif entity_type == "VEHICLE":
        match = find_vehicle(text)

    elif entity_type == "PHONE":
        match = find_phone(text)

    else:
        match = None

    return {
        "text": text,
        "label": entity_type,
        "linked": match is not None,
        "graph_node": match
    }