from graph.database import Neo4jDatabase


def seed_database():

    db = Neo4jDatabase()

    with db.driver.session(database=db.database) as session:

        # Persons
        persons = [
            ("P006", "Arjun Malhotra", 38, "Delhi"),
            ("P007", "Priya Kapoor", 31, "Noida"),
            ("P008", "Karan Bhatia", 44, "Gurgaon"),
            ("P009", "Meera Joshi", 28, "Delhi"),
            ("P010", "Rohan Gupta", 36, "Noida"),
        ]

        for person in persons:
            session.run(
                """
                MERGE (p:Person {id: $id})
                SET p.name = $name,
                    p.age = $age,
                    p.city = $city
                """,
                id=person[0],
                name=person[1],
                age=person[2],
                city=person[3]
            )

        # Phones
        phones = [
            ("PH005", "9000000005"),
            ("PH006", "9000000006"),
            ("PH007", "9000000007"),
            ("PH008", "9000000008"),
        ]

        for phone in phones:
            session.run(
                """
                MERGE (p:Phone {id: $id})
                SET p.number = $number
                """,
                id=phone[0],
                number=phone[1]
            )

        # Vehicles
        vehicles = [
            ("V004", "DL03GH3456", "SUV"),
            ("V005", "UP16JK7890", "Sedan"),
            ("V006", "HR29LM1234", "Hatchback"),
        ]

        for vehicle in vehicles:
            session.run(
                """
                MERGE (v:Vehicle {id: $id})
                SET v.registration = $registration,
                    v.type = $type
                """,
                id=vehicle[0],
                registration=vehicle[1],
                type=vehicle[2]
            )

        # Locations
        locations = [
            ("L005", "Old Delhi Market", "Delhi"),
            ("L006", "Noida Sector 62", "Noida"),
            ("L007", "MG Road", "Gurgaon"),
        ]

        for location in locations:
            session.run(
                """
                MERGE (l:Location {id: $id})
                SET l.name = $name,
                    l.city = $city
                """,
                id=location[0],
                name=location[1],
                city=location[2]
            )

        # Cases
        cases = [
            ("C1004", "Fraud", "2026-08-30", "Open"),
            ("C1005", "Theft", "2026-09-02", "Under Investigation"),
            ("C1006", "Robbery", "2026-09-05", "Open"),
        ]

        for case in cases:
            session.run(
                """
                MERGE (c:Case {id: $id})
                SET c.type = $type,
                    c.date = $date,
                    c.status = $status
                """,
                id=case[0],
                type=case[1],
                date=case[2],
                status=case[3]
            )

        # Person -> Phone
        phone_links = [
            ("P006", "PH005"),
            ("P007", "PH006"),
            ("P008", "PH007"),
            ("P009", "PH005"),
            ("P010", "PH006"),
        ]

        for person_id, phone_id in phone_links:
            session.run(
                """
                MATCH (p:Person {id: $person_id})
                MATCH (ph:Phone {id: $phone_id})
                MERGE (p)-[:USES]->(ph)
                """,
                person_id=person_id,
                phone_id=phone_id
            )

        # Person -> Vehicle
        vehicle_links = [
            ("P006", "V004"),
            ("P007", "V005"),
            ("P008", "V006"),
            ("P009", "V004"),
            ("P010", "V005"),
        ]

        for person_id, vehicle_id in vehicle_links:
            session.run(
                """
                MATCH (p:Person {id: $person_id})
                MATCH (v:Vehicle {id: $vehicle_id})
                MERGE (p)-[:USES]->(v)
                """,
                person_id=person_id,
                vehicle_id=vehicle_id
            )

        # Person -> Location
        location_links = [
            ("P006", "L005"),
            ("P007", "L006"),
            ("P008", "L007"),
            ("P009", "L005"),
            ("P010", "L006"),
        ]

        for person_id, location_id in location_links:
            session.run(
                """
                MATCH (p:Person {id: $person_id})
                MATCH (l:Location {id: $location_id})
                MERGE (p)-[:VISITED]->(l)
                """,
                person_id=person_id,
                location_id=location_id
            )

        # Person -> Case
        case_links = [
            ("P006", "C1004"),
            ("P007", "C1004"),
            ("P008", "C1005"),
            ("P009", "C1005"),
            ("P010", "C1006"),
        ]

        for person_id, case_id in case_links:
            session.run(
                """
                MATCH (p:Person {id: $person_id})
                MATCH (c:Case {id: $case_id})
                MERGE (p)-[:INVOLVED_IN]->(c)
                """,
                person_id=person_id,
                case_id=case_id
            )

        # Case -> Location
        case_locations = [
            ("C1004", "L005"),
            ("C1005", "L006"),
            ("C1006", "L007"),
        ]

        for case_id, location_id in case_locations:
            session.run(
                """
                MATCH (c:Case {id: $case_id})
                MATCH (l:Location {id: $location_id})
                MERGE (c)-[:OCCURRED_AT]->(l)
                """,
                case_id=case_id,
                location_id=location_id
            )

        # Person -> Person
        contacts = [
            ("P006", "P007"),
            ("P007", "P008"),
            ("P008", "P009"),
            ("P009", "P010"),
            ("P006", "P009"),
        ]

        for person1, person2 in contacts:
            session.run(
                """
                MATCH (p1:Person {id: $person1})
                MATCH (p2:Person {id: $person2})
                MERGE (p1)-[:CONTACTED]->(p2)
                """,
                person1=person1,
                person2=person2
            )

    db.close()

    print("Synthetic data added successfully.")


if __name__ == "__main__":
    seed_database()