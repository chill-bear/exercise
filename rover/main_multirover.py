
class Rover:
    DIRECTIONS = ["N", "E", "S", "W"]
    MOVES = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
    }

    def __init__(self, rover_id):
        self.id = rover_id
        self.x = 0
        self.y = 0
        self.direction = "N"

        self.commands = {
            "F": self.move,
            "L": self.turn_left,
            "R": self.turn_right,
        }

    def turn_left(self):
        i = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(i - 1) % 4]

    def turn_right(self):
        i = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(i + 1) % 4]

    def move(self):
        dx, dy = self.MOVES[self.direction]
        self.x += dx
        self.y += dy

    def move_backward(self):
        dx, dy = self.MOVES[self.direction]
        self.x -= dx
        self.y -= dy

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
    # 检查collision
    def execute(self, rover_id, command):
        if rover_id not in self.rovers:
            raise ValueError("Rover not found")

        rover = self.rovers[rover_id]

        if command == "F":
            dx, dy = rover.MOVES[rover.direction]
            new_x = rover.x + dx
            new_y = rover.y + dy

            for other in self.rovers.values():
                if other.id != rover_id:
                    if (other.x, other.y) == (new_x, new_y):
                        raise ValueError("Collision detected")

        rover.execute(command)

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

        rover = self.rovers[rover_id]
        rover.execute(command)


# Create controller
controller = RoverController()

# Create multiple rovers
r1 = Rover("robot1")
r2 = Rover("robot2")

# Register rovers
controller.add_rover(r1)
controller.add_rover(r2)

# Execute commands
controller.execute("robot1", "F")
controller.execute("robot1", "F")

controller.execute("robot2", "R")
controller.execute("robot2", "F")

print(r1.x, r1.y, r1.direction)  # 0 2 N
print(r2.x, r2.y, r2.direction)  # 1 0 E
