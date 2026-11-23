import csv
import random


def load_participants(file_path):
    participants = []

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) < 2:
                raise ValueError(f"Invalid CSV row: {row}")

            name = row[0].strip()
            email = row[1].strip()

            if not name or not email:
                raise ValueError("Name and email cannot be empty")

            participants.append({
                "name": name,
                "email": email,
            })

    return participants


def assign_gifts(participants):
    if len(participants) < 2:
        raise ValueError("At least 2 participants are required")

    shuffled = participants.copy()
    random.shuffle(shuffled)

    assignments = {}

    for i in range(len(shuffled)):
        giver = shuffled[i]["name"]
        if i == len(shuffled) - 1:
            receiver = shuffled[0]["name"]
        else:
            receiver = shuffled[i + 1]["name"]
        # replace line 40-43: receiver = shuffled[(i + 1) % len(shuffled)]["name"]
        assignments[giver] = receiver

    return assignments


def main():
    participants = load_participants("group1.csv")
    assignments = assign_gifts(participants)

    for giver, receiver in assignments.items():
        print(f"{giver} -> {receiver}")


if __name__ == "__main__":
    main()