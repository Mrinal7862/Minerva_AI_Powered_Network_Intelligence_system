import re 

def extract_custom_entities(text:str):
        entities = []

        vehicle_pattern = r"\b[A-Z]{2}\d{2}[A-Z]{2}\d{4}\b"

        for match in re.finditer(vehicle_pattern, text):
                entities.append({
                    "text": match.group(),
                    "label":"VEHICLE"
                })

        phone_pattern = r"\b\d{10}\b"

        for match in re.finditer(phone_pattern, text):
                entities.append({
                        "text":match.group(),
                        "label":"PHONE"
                })

        case_pattern = r"\bC\d{4}\b"

        for match in re.finditer(case_pattern, text):
                entities.append({
                        "text":match.group(),
                        "label":"CASE"
                })

        return entities


if __name__ == "__main__":
        text = """
        Ravi Sharma met Amit Verma at Connaught Place
        using vehicle DL01AB1234.
        Ravi called 9000000001 regarding Case C1001.
        """

        result = extract_custom_entities(text)

        for entity in result:
                print(entity)