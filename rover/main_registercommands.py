
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


rover = Rover()
rover.register_command("B", rover.move_backward)
rover.execute("B")
print(rover.x, rover.y)  # 0, -1
