from neo4j import GraphDatabase
from dotenv import load_dotenv
import os 

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI, 
    auth=(USERNAME, PASSWORD)
)

driver.verify_connectivity()

print("Minerva connected to neo4j")

driver.close()

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