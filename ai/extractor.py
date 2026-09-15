import spacy

nlp = spacy.load("en_core_web_sm")


KNOWN_LOCATIONS = {
    "connaught place",
    "sector 18 market",
    "cyber hub",
    "central warehouse",
    "old delhi market",
    "noida sector 62",
    "mg road"
}

def extract_entities(text: str):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        text_value = ent.text.strip()
        normalized = text_value.lower()

        # Known locations always have LOCATION label
        if normalized in KNOWN_LOCATIONS:
            label = "LOCATION"

        elif ent.label_ == "PERSON":
            label = "PERSON"

        elif ent.label_ in ["GPE", "LOC", "ORG"]:
            label = "LOCATION"

        else:
            continue

        entities.append({
            "text": text_value,
            "label": label
        })

    return entities


if __name__ == "__main__":

    text = """
    Ravi Sharma met Amit Verma at Connaught Place.
    Ravi Sharma visited Connaught Place.
    Ravi Sharma used vehicle DL01AB1234.
    """

    result = extract_entities(text)

    for entity in result:
        print(entity)