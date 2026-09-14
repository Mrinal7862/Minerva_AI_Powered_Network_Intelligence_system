from fastapi import FastAPI
from graph.queries import search_person, get_network, find_shortest_path, get_person_evidence, get_case_connection_evidence
from ai.pipeline import analyze_text
from graph.ingestion import ingest_analysis

app = FastAPI(
    title="Minerva API",
    description = "Investigate Network Intelligence API",
    version = "1.0.0"
)

@app.get("/persons/search")
def search_person_api(name: str):
    return search_person(name)

@app.get("/connections/path")
def connection_path(start_id:str, target_id:str):
    return find_shortest_path(start_id, target_id)

@app.get("/persons/{person_id}/network")
def person_network(person_id: str):
    return get_network(person_id)

@app.get("/persons/{person_id}/evidence")
def person_evidence(person_id: str):
    return get_person_evidence(person_id)

@app.get("/investigator/evidence")
def investigator_evidence(
    person_id: str,
    case_id: str
):
    return get_case_connection_evidence(
        person_id,
        case_id
    )


@app.post("/analyze")
def analyze_investigation(text:str):
    analysis = analyze_text(text)

    ingest_analysis(analysis)

    return analysis