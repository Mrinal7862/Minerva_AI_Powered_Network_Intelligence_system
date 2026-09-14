import re


def extract_contact_relationship(text: str):

    relationships = []

    pattern = (
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
        r"\s+(?:met|called|contacted)\s+"
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*?)"
        r"(?=\s+(?:at|in|on|using|with|regarding)\b|[.,]|$)"
    )

    matches = re.finditer(pattern, text)

    for match in matches:

        relationships.append({
            "source": match.group(1).strip(),
            "relationship": "CONTACTED",
            "target": match.group(2).strip()
        })

    return relationships


def extract_visited_relationship(text: str):

    relationships = []

    pattern = (
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
        r"\s+(?:visited|went to)\s+"
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*?)"
        r"(?=[.,]|$)"
    )

    matches = re.finditer(pattern, text)

    for match in matches:

        relationships.append({
            "source": match.group(1).strip(),
            "relationship": "VISITED",
            "target": match.group(2).strip()
        })

    return relationships


def extract_uses_relationships(text: str):

    relationships = []

    pattern = (
        r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
        r"\s+(?:used|uses)\s+"
        r"(?:vehicle\s+)?"
        r"([A-Z]{2}\d{2}[A-Z]{2}\d{4})"
    )

    matches = re.finditer(pattern, text)

    for match in matches:

        relationships.append({
            "source": match.group(1).strip(),
            "relationship": "USES",
            "target": match.group(2).strip()
        })

    return relationships


def extract_relationships(text: str):

    relationships = []

    relationships.extend(
        extract_contact_relationship(text)
    )

    relationships.extend(
        extract_visited_relationship(text)
    )

    relationships.extend(
        extract_uses_relationships(text)
    )

    return relationships


if __name__ == "__main__":

    text = """
    Ravi Sharma met Amit Verma at Connaught Place.
    Ravi Sharma visited Connaught Place.
    Ravi Sharma used vehicle DL01AB1234.
    """

    result = extract_relationships(text)

    for relationship in result:

        print(relationship)