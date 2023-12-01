from enum import Enum

class Declaration:
    pass

class Tantacule(Declaration):
    def __init__(self, name, instructions, loop):
        self.name = name
        self.instructions = instructions
        self.loop = loop

    def __repr__(self):
        return f"(tantacule (loop = {self.loop}) {self.name} {self.instructions})"

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class MoveDir(Enum):
    FORWARD = 1
    UP = 2
    DOWN = 3

class Instruction():
    pass

class Repeat(Instruction):
    def __init__(self, number, instructions):
        self.number = number
        self.instructions = instructions

    def __repr__(self):
        return f"REPEAT {self.number} {self.instructions}"


class SlideTo(Instruction):
    def __init__(self, tantacule):
        self.tantacule = tantacule

    def __repr__(self):
        return f"SLIDETO {self.tantacule}"

class SlideBack(Instruction):
    def __init__(self):
        pass

    def __repr__(self):
        return f"SLIDEBACK"

class Mark(Instruction):
    def __init__(self, index):
        self.cost = 1
        self.index = index

    def __repr__(self):
        return f"MARK {self.index}"

class Unmark(Instruction):
    def __init__(self, index):
        self.cost = 1
        self.index = index

    def __repr__(self):
        return f"UNMARK {self.index}"

class PickUp(Instruction):
    def __init__(self, handler):
        self.cost = 5
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "PICKUP"
        else:
            return f"PICKUP else {self.handler}"

class Drop(Instruction):
    def __init__(self, handler):
        self.cost = 5
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "DROP"
        else:
            return f"DROP else {self.handler}"

class Turn(Instruction):
    def __init__(self, direction):
        self.cost = 1
        self.direction = direction

    def __repr__(self):
        return f"TURN {self.direction}"

class Move(Instruction):
    def __init__(self, handler, move_dir):
        self.cost = 30
        self.handler = handler
        self.move_dir = move_dir

    def __repr__(self):
        if self.handler is None:
            return f"MOVE {self.move_dir}"
        else:
            return f"MOVE {self.move_dir} else {self.handler}"

class Dig(Instruction):
    def __init__(self, handler, move_dir):
        self.cost = 25
        self.handler = handler
        self.move_dir = move_dir

    def __repr__(self):
        if self.handler is None:
            return f"DIG {self.move_dir}"
        else:
            return f"DIG {self.move_dir} else {self.handler}"

class Fill(Instruction):
    def __init__(self, handler, move_dir):
        self.cost = 25
        self.handler = handler
        self.move_dir = move_dir

    def __repr__(self):
        if self.handler is None:
            return f"FILL {self.move_dir}"
        else:
            return f"FILL {self.move_dir} else {self.handler}"

class Grab(Instruction):
    def __init__(self, handler):
        self.cost = 50
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "GRAB"
        else:
            return f"GRAB else {self.handler}"

class Attack(Instruction):
    def __init__(self, handler):
        self.cost = 30
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "ATTACK"
        else:
            return f"ATTACK else {self.handler}"
