from .database import Neo4jDatabase

LABEL_MAP = {
    "PERSON": "Person",
    "PHONE": "Phone",
    "VEHICLE": "Vehicle",
    "LOCATION": "Location",
    "CASE": "Case",
    "ORG": "Organization"
}

PROPERTY_MAP = {
    "PERSON": "name",
    "PHONE": "number",
    "VEHICLE": "registration",
    "LOCATION": "name",
    "CASE": "id",
    "ORG": "name"
}

def create_entity_in_session(session, entity):

    entity_type = entity["label"]

    label = LABEL_MAP.get(entity_type)
    property_name = PROPERTY_MAP.get(entity_type)

    if label is None or property_name is None:
        return

    value = entity["text"]

    query = f"""
    MERGE (n:{label} {{{property_name}: $value}})
    RETURN n
    """

    session.run(query, value=value)

def find_entity_id(session, entity):

    entity_type = entity["label"]
    value = entity["text"]

    label = LABEL_MAP.get(entity_type)
    property_name = PROPERTY_MAP.get(entity_type)

    if label is None or property_name is None:
        return None

    query = f"""
    MATCH (n:{label} {{{property_name}: $value}})
    RETURN n.id AS id
    LIMIT 1
    """

    result = session.run(
        query,
        value=value
    )

    record = result.single()

    if record:
        return record["id"]

    return None
def create_relationship_in_session(session, relationship):

    source = relationship["source"]
    relation = relationship["relationship"]
    target = relationship["target"]

    source_query = """
    MATCH (a)
    WHERE
        a.name = $value OR
        a.number = $value OR
        a.registration = $value OR
        a.id = $value
    RETURN a
    LIMIT 1
    """

    target_query = """
    MATCH (b)
    WHERE
        b.name = $value OR
        b.number = $value OR
        b.registration = $value OR
        b.id = $value
    RETURN b
    LIMIT 1
    """

    source_result = session.run(
        source_query,
        value=source
    ).single()

    target_result = session.run(
        target_query,
        value=target
    ).single()

    if source_result is None or target_result is None:
        return

    source_node = source_result["a"]
    target_node = target_result["b"]

    query = f"""
    MATCH (a), (b)
    WHERE elementId(a) = $source_element_id
      AND elementId(b) = $target_element_id
    MERGE (a)-[:{relation}]->(b)
    """

    session.run(
        query,
        source_element_id=source_node.element_id,
        target_element_id=target_node.element_id
    )

def ingest_analysis(analysis):

    db = Neo4jDatabase()

    with db.driver.session(database=db.database) as session:

        for entity in analysis["entities"]:
            create_entity_in_session(session, entity)

        for relationship in analysis["relationships"]:
            create_relationship_in_session(session, relationship)

    db.close()