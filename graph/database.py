from neo4j import GraphDatabase
from dotenv import load_dotenv
import os 

load_dotenv()

class Neo4jDatabase:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def verify_connection(self):
        self.driver.verify_connectivity()
        print("MINERVA -> NEO4J CONNECTED")

    def close(self):
        self.driver.close()

if __name__ == '__main__':
    db = Neo4jDatabase()
    db.verify_connection()
    db.close()