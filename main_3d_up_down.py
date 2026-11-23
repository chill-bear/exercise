
class Rover:
    DIRECTIONS = ["N", "E", "S", "W"]

    MOVES = {
        "N": (0, 1, 0),
        "E": (1, 0, 0),
        "S": (0, -1, 0),
        "W": (-1, 0, 0),
        "U": (0, 0, 1),
        "D": (0, 0, -1),
    }

    def __init__(self, rover_id):
        self.id = rover_id
        self.x = 0
        self.y = 0
        self.z = 0
        self.direction = "N"

        self.commands = {
            "F": self.move,
            "L": self.turn_left,
            "R": self.turn_right,
            "PITCH_UP": self.pitch_up,
            "PITCH_DOWN": self.pitch_down,
        }

    def turn_left(self):
        if self.direction not in self.DIRECTIONS:
            raise ValueError("Cannot turn left while facing U/D")

        i = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(i - 1) % 4]

    def turn_right(self):
        if self.direction not in self.DIRECTIONS:
            raise ValueError("Cannot turn right while facing U/D")

        i = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(i + 1) % 4]

    def pitch_up(self):
        if self.direction == "U":
            self.direction = "S"
        elif self.direction == "D":
            self.direction = "N"
        elif self.direction == "N":
            self.direction = "U"
        elif self.direction == "S":
            self.direction = "D"
        else:
            raise ValueError("Pitch not supported for E/W")

    def pitch_down(self):
        if self.direction == "U":
            self.direction = "N"
        elif self.direction == "D":
            self.direction = "S"
        elif self.direction == "N":
            self.direction = "D"
        elif self.direction == "S":
            self.direction = "U"
        else:
            raise ValueError("Pitch not supported for E/W")

    def move(self):
        dx, dy, dz = self.MOVES[self.direction]
        self.x += dx
        self.y += dy
        self.z += dz

    def move_backward(self):
        dx, dy, dz = self.MOVES[self.direction]
        self.x -= dx
        self.y -= dy
        self.z -= dz

    def register_command(self, name, handler):
        if not callable(handler):
            raise TypeError("Handler must be callable")

        if name in self.commands:
            raise ValueError("Command already registered")

        self.commands[name] = handler

    def execute(self, command):
        handler = self.commands.get(command)

        if handler is None:
            raise ValueError(f"Unknown command: {command}")

        handler()

    def position(self):
        return self.x, self.y, self.z, self.direction


class RoverController:
    def __init__(self):
        self.rovers = {}

    def add_rover(self, rover):
        if rover.id in self.rovers:
            raise ValueError("Rover already exists")

        self.rovers[rover.id] = rover

    def execute(self, rover_id, command):
        if rover_id not in self.rovers:
            raise ValueError("Rover not found")

        self.rovers[rover_id].execute(command)


# Test
controller = RoverController()

r1 = Rover("robot1")
r2 = Rover("robot2")

controller.add_rover(r1)
controller.add_rover(r2)

controller.execute("robot1", "F")
controller.execute("robot1", "PITCH_UP")
controller.execute("robot1", "F")

controller.execute("robot2", "R")
controller.execute("robot2", "F")

print(r1.position())  # (0, 1, 1, 'U')
print(r2.position())  # (1, 0, 0, 'E')
