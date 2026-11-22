
class Rover:
    DIRECTIONS = ["N", "E", "S", "W"]

    MOVES = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
    }

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = "N"

    def turn_left(self):
        index = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(index - 1) % 4]

    def turn_right(self):
        index = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(index + 1) % 4]

    def move(self):
        dx, dy = self.MOVES[self.direction]
        self.x += dx
        self.y += dy

    def execute(self, command):
        if command == "L":
            self.turn_left()
        elif command == "R":
            self.turn_right()
        elif command == "M":
            self.move()
        else:
            raise ValueError(f"Invalid command: {command}")

    def position(self):
        return self.x, self.y, self.direction


def main():
    rover = Rover()

    while True:
        commands = input("Enter commands (or Q to quit): ").strip().upper()

        if commands == "Q":
            break

        for command in commands:
            try:
                rover.execute(command)
                print(rover.position())
            except ValueError as error:
                print(error)


if __name__ == "__main__":
    main()
