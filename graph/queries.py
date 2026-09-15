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

    with db.driver.session(database=db.database) as session:
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
    (p:Person {id: $person_id})
    -[*..6]-
    (c:Case {id: $case_id})

    WITH path
    ORDER BY length(path)
    LIMIT 1

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

def get_shared_connections():
    db = Neo4jDatabase()

    query = """
    MATCH (p1:Person)-[:USES]->(resource)<-[:USES]-(p2:Person)
    WHERE p1.id < p2.id

    RETURN
        p1.id AS person1_id,
        p1.name AS person1_name,
        labels(resource)[0] AS resource_type,
        resource.id AS resource_id,
        resource.number AS resource_number,
        resource.registration AS resource_registration,
        p2.id AS person2_id,
        p2.name AS person2_name

    ORDER BY resource_type
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(query)
        connections = [record.data() for record in result]

    db.close()

    return connections

def get_person_centrality():
    db = Neo4jDatabase()

    query = """
    MATCH (p:Person)
    OPTIONAL MATCH (p)-[r]-()
    WITH p, count(r) AS connections
    RETURN
        p.id AS person_id,
        p.name AS person_name,
        connections
    ORDER BY connections DESC
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(query)
        centrality = [record.data() for record in result]

    db.close()

    return centrality

def get_communities():
    db = Neo4jDatabase()

    query = """
    MATCH (p1:Person)-[*1..3]-(p2:Person)
    WHERE p1.id < p2.id

    WITH p1, p2, count(*) AS strength

    RETURN
        p1.id AS person1_id,
        p1.name AS person1_name,
        p2.id AS person2_id,
        p2.name AS person2_name,
        strength

    ORDER BY strength DESC
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(query)
        communities = [record.data() for record in result]

    db.close()

    return communities

def get_case_timeline():
    db = Neo4jDatabase()

    query = """
    MATCH (c:Case)
    OPTIONAL MATCH (c)-[:OCCURRED_AT]->(l:Location)

    RETURN
        c.id AS case_id,
        c.type AS case_type,
        c.date AS date,
        c.status AS status,
        l.id AS location_id,
        l.name AS location_name

    ORDER BY c.date
    """

    with db.driver.session(database=db.database) as session:
        result = session.run(query)
        timeline = [record.data() for record in result]

    db.close()

    return timeline