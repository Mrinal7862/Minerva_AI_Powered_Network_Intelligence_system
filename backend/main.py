from fastapi import FastAPI
from graph.queries import (
    search_person,
    get_network,
    find_shortest_path,
    get_person_evidence,
    get_case_connection_evidence,
    get_shared_connections,
    get_person_centrality,
    get_communities,
    get_case_timeline
                            )

from ai.pipeline import analyze_text
from graph.ingestion import ingest_analysis
from ai.investigator import generate_investigation_answer


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

@app.get("/investigator/ask")
def ask_investigator(question:str, person_id: str, case_id:str):

    evidence = get_case_connection_evidence(
        person_id,
        case_id
    )

    if evidence is None:
        return {
            "answer" : "No connection or sufficient evidence found",
            "evidence": None
        }

    answer = generate_investigation_answer(
        question,
        evidence
    )

    return {
        "answer":answer,
        "evidence":evidence
    }

@app.get("/analytics/shared-connections")
def shared_connections():
    return get_shared_connections()

@app.get("/analytics/centrality")
def person_centrality():
    return get_person_centrality()

@app.get("/analytics/communities")
def communities():
    return get_communities

@app.get("/analytics/timeline")
def case_timeline():
    return get_case_timeline()