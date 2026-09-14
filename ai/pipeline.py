from .extractor import extract_entities
from .custom_entity import extract_custom_entities
from .relationship_extractor import extract_relationships


def normalize_text(value):
    return " ".join(value.split())


def analyze_text(text: str):

    # -----------------------------
    # 1. Extract entities
    # -----------------------------
    entities = extract_entities(text)
    custom_entities = extract_custom_entities(text)
    relationships = extract_relationships(text)

    # -----------------------------
    # 2. Custom entities have priority
    # -----------------------------
    custom_texts = {
        normalize_text(entity["text"]).lower()
        for entity in custom_entities
    }

    filtered_entities = [
        entity
        for entity in entities
        if normalize_text(entity["text"]).lower()
        not in custom_texts
    ]

    all_entities = filtered_entities + custom_entities

    # -----------------------------
    # 3. Remove duplicate entities
    # -----------------------------
    unique_entities = []
    seen = set()

    for entity in all_entities:

        text_value = normalize_text(entity["text"])
        label = entity["label"]

        key = (text_value.lower(), label)

        if key in seen:
            continue

        seen.add(key)

        unique_entities.append({
            "text": text_value,
            "label": label
        })

    # -----------------------------
    # 4. Add entities from relationships
    # -----------------------------
    existing_names = {
        entity["text"].lower()
        for entity in unique_entities
    }

    for relationship in relationships:

        source = normalize_text(relationship["source"])
        target = normalize_text(relationship["target"])
        relation = relationship["relationship"]

        # Source of our current relationships is always PERSON
        if source.lower() not in existing_names:

            unique_entities.append({
                "text": source,
                "label": "PERSON"
            })

            existing_names.add(source.lower())

        # Decide target type from relationship
        if relation == "CONTACTED":

            target_label = "PERSON"

        elif relation == "VISITED":

            target_label = "LOCATION"

        elif relation == "USES":

            target_label = "VEHICLE"

        else:

            target_label = "PERSON"

        # IMPORTANT:
        # If target already exists with another label,
        # do not create another entity.
        if target.lower() not in existing_names:

            unique_entities.append({
                "text": target,
                "label": target_label
            })

            existing_names.add(target.lower())

    # -----------------------------
    # 5. Return final analysis
    # -----------------------------
    return {
        "entities": unique_entities,
        "relationships": relationships
    }


if __name__ == "__main__":

    text = """
    Ravi Sharma met Amit Verma at Connaught Place.
    Ravi Sharma visited Connaught Place.
    Ravi Sharma used vehicle DL01AB1234.
    Ravi called 9000000001 regarding Case C1001.
    """

    result = analyze_text(text)

    print("\nENTITIES")

    for entity in result["entities"]:
        print(entity)

    print("\nRELATIONSHIPS")

    for relationship in result["relationships"]:
        print(relationship)