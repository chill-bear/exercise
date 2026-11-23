import csv
import random


def load_participants(file_path):
    participants = []
    names = set()

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row or all(not cell.strip() for cell in row):
                continue

            if len(row) < 2:
                raise ValueError(f"Invalid CSV row: {row}")

            name = row[0].strip()
            email = row[1].strip()

            # Ignore empty trailing exclusion columns
            exclusions = {
                value.strip()
                for value in row[2:]
                if value.strip()
            }

            if not name or not email:
                raise ValueError("Name and email cannot be empty")

            if name in names:
                raise ValueError(f"Duplicate participant: {name}")

            names.add(name)

            participants.append({
                "name": name,
                "email": email,
                "exclusions": exclusions,
            })

    # Validate exclusion references
    for person in participants:
        unknown = person["exclusions"] - names
        if unknown:
            raise ValueError(
                f"Unknown exclusions for {person['name']}: {unknown}"
            )

    return participants


def assign_gifts(participants):
    if len(participants) < 2:
        raise ValueError("At least 2 participants are required")

    names = [person["name"] for person in participants]

    exclusions = {
        person["name"]: person["exclusions"]
        for person in participants
    }

    # Randomize giver order
    givers = names.copy()
    random.shuffle(givers)

    assignments = {}
    used_receivers = set()

    def backtrack(index):
        if index == len(givers):
            return True

        giver = givers[index]

        # Randomize receiver candidates
        candidates = names.copy()
        random.shuffle(candidates)

        for receiver in candidates:
            if receiver == giver:
                continue

            if receiver in used_receivers:
                continue

            if giver in exclusions[receiver]:
                continue

            assignments[giver] = receiver
            used_receivers.add(receiver)

            if backtrack(index + 1):
                return True

            # Undo assignment
            del assignments[giver]
            used_receivers.remove(receiver)

        return False

    if not backtrack(0):
        raise ValueError("No valid gift assignment exists")

    return assignments


def main():
    participants = load_participants("group2.csv")
    assignments = assign_gifts(participants)

    print("Holiday Gift Exchange Results:")

    for giver, receiver in assignments.items():
        print(f"{giver} -> {receiver}")


if __name__ == "__main__":
    main()