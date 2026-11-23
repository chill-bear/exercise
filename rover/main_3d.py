
class Rover:
    DIRECTIONS = ["N", "E", "S", "W"]

    MOVES = {
        "N": (0, 1, 0),
        "E": (1, 0, 0),
        "S": (0, -1, 0),
        "W": (-1, 0, 0),
    }

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.direction = "N"

        self.commands = {
            "F": self.move,
            "L": self.turn_left,
            "R": self.turn_right,
            "U": self.move_up,
            "D": self.move_down,
        }

    def turn_left(self):
        i = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(i - 1) % 4]

    def turn_right(self):
        i = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(i + 1) % 4]

    def move(self):
        dx, dy, dz = self.MOVES[self.direction]
        self.x += dx
        self.y += dy
        self.z += dz

    def move_up(self):
        self.z += 1

    def move_down(self):
        self.z -= 1

    def execute(self, command):
        handler = self.commands.get(command)

        if handler is None:
            raise ValueError(f"Unknown command: {command}")

        handler()


rover = Rover()

rover.execute("F")  # (0, 1, 0)
rover.execute("U")  # (0, 1, 1)
rover.execute("R")  # Facing East
rover.execute("F")  # (1, 1, 1)

print(rover.x, rover.y, rover.z, rover.direction)
# 1 1 1 E
