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