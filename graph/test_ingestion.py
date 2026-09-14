from ai.pipeline import analyze_text
from graph.ingestion import ingest_analysis


text = """
Ravi Sharma met Amit Verma at Connaught Place.
Ravi Sharma visited Connaught Place.
Ravi Sharma used vehicle DL01AB1234.
"""

analysis = analyze_text(text)

print("\nANALYSIS:")
print(analysis)

ingest_analysis(analysis)

print("\nData successfully ingested into Neo4j.")