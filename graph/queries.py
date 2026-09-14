from .database import Neo4jDatabase


def search_person(name:str):
    db = Neo4jDatabase()

    query = """
         MATCH (p:Person)
    WHERE toLower(p.name) CONTAINS toLower($name)
    RETURN p.id AS id,
           p.name AS name,
           p.age AS age,
           p.city AS city
        
    """
    with db.driver.session(database=db.database) as session:
        result = session.run(query, name=name)
        person = [record.data() for record in result]

    db.close()
    return person

def get_person_connections(person_id:str):
    db = Neo4jDatabase()

    query = """
        MATCH (p:Person {id:$person_id})-[r]-(connected)
        RETURN
            connected.id AS id,
            labels(connected) AS type,
            connected.name AS name,
            type(r) AS relationship
"""

    with db.driver.session(database=db.database) as session:
        result = session.run(query, person_id=person_id)
        connections = [record.data() for  record in result]

    db.close()
    return connections

def get_network(person_id: str):
    db = Neo4jDatabase()

    query = """
    MATCH (p:Person {id: $person_id})-[r]-(connected)
    RETURN
        p.id AS source_id,
        p.name AS source_name,
        type(r) AS relationship,
        labels(connected) AS target_type,
        connected.id AS target_id,
        connected.name AS target_name
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(query, person_id=person_id)
        network = [record.data() for record in result]


    db.close()

    return network

def find_shortest_path(start_id: str, target_id:str):
    db = Neo4jDatabase()

    query= """
    MATCH path =
    shortestPath(
        (start:Person {id: $start_id})
        -[*..6]-
        (target:Case {id: $target_id})
    )
    RETURN [node IN nodes(path) | {
        id: node.id,
        name: node.name,
        type: labels(node)
    }] AS nodes,
    [rel IN relationships(path) | type(rel)] AS relationships
    """

    with db.driver.session(databe=db.database) as session:
        result = session.run(
            query,
            start_id=start_id,
            target_id=target_id
        )

        record = result.single()

    db.close()

    if record is None:
        return None

    return record.data()

def get_person_evidence(person_id: str):

    db = Neo4jDatabase()

    query = """
    MATCH (p:Person {id: $person_id})
    OPTIONAL MATCH (p)-[r]-(connected)

    RETURN
        p.id AS person_id,
        p.name AS person_name,
        p.age AS age,
        p.city AS city,
        collect({
            relationship: type(r),
            connected_id: connected.id,
            connected_name: connected.name,
            connected_number: connected.number,
            connected_registration: connected.registration,
            connected_type: labels(connected)
        }) AS connections
    """

    with db.driver.session(database=db.database) as session:

        result = session.run(
            query,
            person_id=person_id
        )

        record = result.single()

    db.close()

    if record is None:
        return None

    return record.data()

def get_case_connection_evidence(person_id: str, case_id: str):

    db = Neo4jDatabase()

    query = """
    MATCH path =
    shortestPath(
        (p:Person {id: $person_id})
        -[*..6]-
        (c:Case {id: $case_id})
    )

    RETURN
        [node IN nodes(path) | {
            id: node.id,
            name: node.name,
            type: labels(node)[0],
            number: node.number,
            registration: node.registration
        }] AS nodes,

        [rel IN relationships(path) | type(rel)] AS relationships
    """

    with db.driver.session(database=db.database) as session:

        result = session.run(
            query,
            person_id=person_id,
            case_id=case_id
        )

        record = result.single()

    db.close()

    if record is None:
        return None

    return record.data()