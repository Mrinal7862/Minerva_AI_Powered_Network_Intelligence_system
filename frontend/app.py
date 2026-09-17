import streamlit as st
import requests
from pyvis.network import Network
import streamlit.components.v1 as components
import os

API_URL = os.getenv("MINERVA_API_URL", "http://127.0.0.1:8000")
API_URL = os.getenv("MINERVA_API_URL", "http://127.0.0.1:8000")

#page config
st.set_page_config(
    page_title="Minerva",
    page_icon="search",
    layout="wide"
)


# =========================
# MINERVA DASHBOARD STYLE
# =========================

st.markdown("""
<style>

    .stApp {
        background: #0b0f14;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .minerva-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 0;
    }

    .minerva-subtitle {
        color: #8b96a5;
        font-size: 1.05rem;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .dashboard-card {
        background: #111720;
        border: 1px solid #202936;
        border-radius: 12px;
        padding: 18px;
        min-height: 100px;
    }

    .card-label {
        color: #7f8a99;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    .card-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 5px;
    }

    .section-label {
        color: #7f8a99;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 10px;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    .minerva-loader {
        padding: 20px;
        text-align: center;
        border: 1px solid #263241;
        border-radius: 12px;
        background: #111720;
        margin: 15px 0;
    }

    .loader-icon {
        font-size: 32px;
        animation: pulse 1.2s infinite;
    }

    .loader-text {
        margin-top: 8px;
        font-size: 16px;
        letter-spacing: 1px;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 0.5;
        }

        50% {
            transform: scale(1.25);
            opacity: 1;
        }

        100% {
            transform: scale(1);
            opacity: 0.5;
        }
    }

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="minerva-title">🕵️ MINERVA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="minerva-subtitle">'
    'AI-Powered Investigative Network Intelligence <br>Note MINERVA is demonstrated on synthetic investigative data to ensure privacy and safe evaluation; the same pipeline can ingest real investigation datasets when provided through authorized data sources'
    '</div>',
    unsafe_allow_html=True
)


# =========================
# DASHBOARD STATUS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-label">Platform</div>
        <div class="card-value">MINERVA</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-label">Knowledge Graph</div>
        <div class="card-value">Neo4j</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-label">AI Engine</div>
        <div class="card-value">Gemini</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-label">Status</div>
        <div class="card-value">● Online</div>
    </div>
    """, unsafe_allow_html=True)


st.divider()


# =========================
# HEADER
# =========================

st.title("Minerva")
st.subheader("AI-Powered Investigative Network Intelligence")

st.divider()


# =========================
# INVESTIGATION INPUT
# =========================

st.header("Investigation Input")

text = st.text_area(
    "Enter investigation text",
    placeholder=(
        "Example: Ravi Sharma met Amit Verma at Connaught Place..."
    )
)


if st.button("Analyze"):

    if not text.strip():
        st.warning("Please enter investigation text.")

    else:

        response = requests.post(
            f"{API_URL}/analyze",
            params={
                "text": text
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Analysis Completed...")

            st.subheader("Entities")
            st.json(result["entities"])

            st.subheader("Relationships")
            st.json(result["relationships"])

        else:

            st.error("Backend error.")


st.divider()
# =========================
# INVESTIGATION INPUT
# =========================

st.markdown(
    '<div class="section-label">DATA INGESTION</div>',
    unsafe_allow_html=True
)

st.header("📝 Investigation Input")

st.write(
    "Enter raw investigation information to extract entities "
    "and relationships automatically."
)

text = st.text_area(
    "Investigation Text",
    placeholder=(
        "Example:\n"
        "Ravi Sharma met Amit Verma at Connaught Place.\n"
        "Ravi Sharma used vehicle DL01AB1234."
    ),
    height=150,
    label_visibility="collapsed"
)

analyze_clicked = st.button(
    "🧠 Analyze Investigation",
    use_container_width=True
)

if analyze_clicked:

    if not text.strip():

        st.warning("Please enter investigation text.")

    else:

        with st.spinner(
            "🧠 MINERVA is extracting investigation intelligence..."
        ):

            response = requests.post(
                f"{API_URL}/analyze",
                params={
                    "text": text
                }
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Investigation analysis completed.")

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.subheader("👤 Entities")

                st.json(
                    result["entities"],
                    expanded=False
                )

            with result_col2:

                st.subheader("🔗 Relationships")

                st.json(
                    result["relationships"],
                    expanded=False
                )

        else:

            st.error(
                f"Backend analysis failed "
                f"(HTTP {response.status_code})"
            )
            
# =========================
# NETWORK GRAPH
# =========================

if "selected_person" in st.session_state:

    person = st.session_state["selected_person"]

    st.divider()

    st.header("Investigation Network")

    response = requests.get(
        f"{API_URL}/persons/{person['id']}/network"
    )

    if response.status_code == 200:

        network = response.json()

        graph = Network(
            height="600px",
            width="100%",
            bgcolor="#0E1117",
            font_color="white"
        )

        # Target person
        graph.add_node(
            person["id"],
            label=person["name"],
            title="Person",
            size=30
        )

        # Connected nodes
        for connection in network:

            target_id = connection["target_id"]

            target_name = (
                connection["target_name"]
                or target_id
            )

            graph.add_node(
                target_id,
                label=target_name,
                title=str(connection["target_type"]),
                size=20
            )

            graph.add_edge(
                person["id"],
                target_id,
                label=connection["relationship"]
            )

        graph.toggle_physics(True)

        graph_file = "frontend/network.html"

        graph.save_graph(graph_file)

        components.html(
            open(
                graph_file,
                "r",
                encoding="utf-8"
            ).read(),
            height=600
        )

    else:

        st.error("Could not load network.")


st.divider()



# FIND HIDDEN CONNECTION


st.header("🔗 Find Hidden Connection")

start_id = st.text_input(
    "Person ID",
    value="P001"
)

target_id = st.text_input(
    "Case ID",
    value="C1003"
)


if st.button("Find Connection"):

    response = requests.get(
        f"{API_URL}/connections/path",
        params={
            "start_id": start_id,
            "target_id": target_id
        }
    )

    if response.status_code == 200:

        path = response.json()

        if path:

            st.success("Connection found!")

            st.subheader("Investigation Path")

            nodes = path["nodes"]
            relationships = path["relationships"]

            for i, node in enumerate(nodes):

                st.write(
                    f"**{node['name'] or node['id']}** "
                    f"({node['type'][0]})"
                )

                if i < len(relationships):

                    st.write(
                        f"↓ **{relationships[i]}**"
                    )

        else:

            st.warning("No connection found.")

    else:

        st.error("Could not find connection.")



# AI INVESTIGATOR


st.divider()

st.header("🤖 AI Investigator")

st.write(
    "Ask a question about a person and case. "
    "MINERVA will answer using evidence from the knowledge graph."
)

ai_person_id = st.text_input(
    "Person ID",
    value="P001",
    key="ai_person_id"
)

ai_case_id = st.text_input(
    "Case ID",
    value="C1003",
    key="ai_case_id"
)

question = st.text_area(
    "Investigation Question",
    value="How is Ravi Sharma connected to Case C1003?",
    height=100,
    key="investigator_question"
)

if st.button("🧠 Ask MINERVA", use_container_width=True):

    if not ai_person_id.strip() or not ai_case_id.strip():
        st.warning("Please enter Person ID and Case ID.")

    elif not question.strip():
        st.warning("Please enter an investigation question.")

    else:

        with st.spinner("🧠 MINERVA is analyzing the investigation..."):

            response = requests.get(
                f"{API_URL}/investigator/ask",
                params={
                    "question": question,
                    "person_id": ai_person_id.strip(),
                    "case_id": ai_case_id.strip()
                }
            )
        if response.status_code == 200:

            result = response.json()

            st.subheader("💡 Investigation Result")

            st.write(result["answer"])

            if result.get("evidence"):

                st.subheader("📌 Evidence Path")

                nodes = result["evidence"]["nodes"]
                relationships = result["evidence"]["relationships"]

                for i, node in enumerate(nodes):

                    node_name = node["name"] or node["id"]

                    st.write(
                        f"**{node_name}** "
                        f"({node['type']})"
                    )

                    if i < len(relationships):

                        st.write(
                            f"↓ **{relationships[i]}**"
                        )

        else:

            st.error(
                f"AI Investigator failed "
                f"(HTTP {response.status_code})"
            )


# SHARED CONNECTIONS

st.divider()

st.header("🔗 Shared Connections")

st.write(
    "Discover people who share common phones or vehicles."
)

if st.button("🔍 Analyze Shared Connections", use_container_width=True):

    with st.spinner("🧠 MINERVA is analyzing shared resources..."):

        response = requests.get(
            f"{API_URL}/analytics/shared-connections"
        )

    if response.status_code == 200:

        connections = response.json()

        if not connections:

            st.info("No shared connections found.")

        else:

            st.success(
                f"{len(connections)} shared connection(s) discovered."
            )

            for connection in connections:

                resource_type = connection["resource_type"]

                if resource_type == "Phone":

                    resource = connection["resource_number"]
                    icon = "📱"

                elif resource_type == "Vehicle":

                    resource = connection["resource_registration"]
                    icon = "🚗"

                else:

                    resource = (
                        connection["resource_id"]
                        or "Unknown"
                    )
                    icon = "🔗"

                st.markdown(
                    f"""
                    **{connection["person1_name"]}**
                    ↔ **{connection["person2_name"]}**

                    {icon} **{resource_type}:** `{resource}`
                    """
                )

                st.divider()

    else:

        st.error("Could not analyze shared connections.")


# NETWORK INTELLIGENCE

st.divider()

st.header("📊 Network Intelligence")

st.write(
    "Identify highly connected people in the investigation network."
)

if st.button(
    "📈 Analyze Network",
    use_container_width=True
):

    with st.spinner("🧠 MINERVA is analyzing network structure..."):

        response = requests.get(
            f"{API_URL}/analytics/centrality"
        )

    if response.status_code == 200:

        centrality = response.json()

        # Keep only valid Person nodes
        centrality = [
            person
            for person in centrality
            if person.get("person_id")
        ]

        if not centrality:

            st.info("No network data available.")

        else:

            st.success(
                f"{len(centrality)} people analyzed."
            )

            for index, person in enumerate(centrality):

                rank = index + 1

                col1, col2, col3 = st.columns(
                    [1, 5, 2]
                )

                with col1:
                    st.markdown(
                        f"### #{rank}"
                    )

                with col2:
                    st.markdown(
                        f"**{person['person_name']}**"
                    )

                    st.caption(
                        f"ID: {person['person_id']}"
                    )

                with col3:
                    st.metric(
                        "Connections",
                        person["connections"]
                    )

                st.divider()


# INVESTIGATION TIMELINE
st.divider()

st.markdown(
    '<div class="section-label">TEMPORAL ANALYSIS</div>',
    unsafe_allow_html=True
)

st.header("🕐 Investigation Timeline")

st.write(
    "Review investigation cases chronologically with their "
    "locations and current status."
)

if st.button(
    "🕐 Load Timeline",
    use_container_width=True
):

    with st.spinner("🧠 MINERVA is building the investigation timeline..."):

        response = requests.get(
           f"{API_URL}/analytics/timeline"
        )

    if response.status_code == 200:

        timeline = response.json()

        if not timeline:

            st.info("No timeline data available.")

        else:

            for event in timeline:

                st.markdown(
                    f"""
                    **{event["date"]}** — **{event["case_id"]}**

                    **Type:** {event["case_type"]}  
                    **Status:** {event["status"]}  
                    **Location:** {event["location_name"]}
                    """
                )

                st.divider()

    else:

        st.error("Could not load investigation timeline.")