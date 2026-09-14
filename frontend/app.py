import streamlit as st
import requests
from pyvis.network import Network
import streamlit.components.v1 as components



st.set_page_config(
    page_title = "Minerva",
    page_icon = "search",
    layout = "wide"
)


st.title("Minerva") 
st.subheader("AI-Powered Investigative Network Intelligence")

st.divider()

st.header("Investigation Input")

text = st.text_area(
    "Enter investigation text",
    placeholder="Example: Ravi sharma met Amit verma at connaught place..."
)

if st.button("Analyze"):
    if not text.strip():
        st.warning("Please enter investigation text.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            params={"text":text}            
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Analysis Completed...")
            st.subheader("Entites")
            st.json(result['entities'])
            st.subheader("Relationships")
            st.json(result['relationships'])

        else:
            st.error("Backend error.")

st.divider()


st.header("Investigate Person")

person_name = st.text_input(
    "Search Person",
    placeholder = "Example: Ravi Sharma"
)

if st.button("Search Person"):
    if not person_name.strip():
        st.warning("Enter a person's name.")
    else:
        response = requests.get(
            "http://127.0.0.1:8000/persons/search",
            params={"name": person_name}
        )

        if response.status_code == 200:
            persons = response.json()

            if not persons:
                st.warning("No person found")
            else:
                person = persons[0]

                st.success(
                    f"Found: {person['name']}({person['id']})"
                )

                st.session_state["selected_person"] = person

        else:
            st.error("Search failed")


# Network graph

if "selected_person" in st.session_state:
    person = st.session_state["selected_person"]

    st.divider()

    st.header("Investigation Network")

    response = requests.get(
        f"http://127.0.0.1:8000/persons/{person['id']}/network"
    )

    if response.status_code == 200:
        network = response.json()

        graph = Network(
            height = "600px",
            width = "100%",
            bgcolor="#0E1117",
            font_color="white"
        )

        # target person 
        graph.add_node(
            person["id"],
            label = person["name"],
            title="Person",
            size=30
        )

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
            open(graph_file, "r", encoding="utf-8").read(),
            height=600
        )
    else:
        st.error("Could not load network.")

st.divider()

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
        "http://127.0.0.1:8000/connections/path",
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