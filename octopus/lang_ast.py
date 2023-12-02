from enum import Enum

class Program:
    def __init__(self, declarations):
        self.declarations = declarations
        self.tantacules = {}
        for declaration in declarations:
            self.tantacules[declaration.name] = declaration

    def __repr__(self):
        return self.declarations.__repr__()

    def accept(self, visitor):
        visitor.visit_program(self)


class Declaration:
    pass

class Tantacule(Declaration):
    def __init__(self, name, instructions, loop):
        self.location_span = None
        self.name = name
        self.instructions = instructions
        self.loop = loop

    def __repr__(self):
        return f"(tantacule (loop = {self.loop}) {self.name} {self.instructions})"

    def accept(self, visitor):
        visitor.visit_tantacule(self)

class Macro(Declaration):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"(macro {self.name} {self.instructions})"

    def accept(self, visitor):
        visitor.visit_macro(self)


class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class MoveDir(Enum):
    FORWARD = 1
    UP = 2
    DOWN = 3

class SenseDir(Enum):
    HERE = 1
    AHEAD = 2
    LEFTAHEAD = 3
    RIGHTAHEAD = 4
    ABOVE = 5
    BELOW = 6

class Smell:
    pass

class AtomicSmell(Smell, Enum):
    FRIEND = 1
    ENEMY = 2
    GRABBED = 3
    FRIENDWITHFOOD = 4
    ENEMYWITHFOOD = 5
    FOOD = 6
    ROCK = 7
    EMPTY = 8
    UNDERGROUND = 9
    SURFACE = 10
    HOLEABOVE = 11
    HOLEBELOW = 12
    ENEMYMARKER = 13
    HOME = 14
    ENEMYHOME = 14

class Marker(Smell):
    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return f"(Marker {self.index})"


class Condition:
    pass

class Sense(Condition):
    def __init__(self, smell, sense_dir):
        self.smell = smell
        self.sense_dir = sense_dir

    def __repr__(self):
        return f"(? {self.smell} {self.sense_dir})"

    def accept(self, visitor):
        visitor.visit_sense(self)

class Rand(Condition):
    def __init__(self, faces_count):
        self.faces_count = faces_count

    def __repr__(self):
        return f"(rand {self.faces_count})"

    def accept(self, visitor):
        visitor.visit_rand(self)

class Not(Condition):
    def __init__(self, condition):
        self.condition = condition

    def __repr__(self):
        return f"(not {self.condition})"

    def accept(self, visitor):
        visitor.visit_not(self)

class Or(Condition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(or {self.left} {self.right})"

    def accept(self, visitor):
        visitor.visit_or(self)

class And(Condition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(and {self.left} {self.right})"

    def accept(self, visitor):
        visitor.visit_and(self)

class Instruction():
    pass

class Repeat(Instruction):
    def __init__(self, number, instructions):
        self.number = number
        self.instructions = instructions

    def __repr__(self):
        return f"REPEAT {self.number} {self.instructions}"

    def accept(self, visitor):
        visitor.visit_repeat(self)

class IfThenElse(Instruction):
    def __init__(self, condition, then, else_):
        self.condition = condition
        self.then = then
        self.else_ = else_

    def __repr__(self):
        return f"(ifthenelse {self.condition} {self.then} {self.else_})"

    def accept(self, visitor):
        visitor.visit_ifthenelse(self)

class While(Instruction):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __repr__(self):
        return f"(while {self.condition} {self.instructions})"

    def accept(self, visitor):
        visitor.visit_while(self)

class Call(Instruction):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"CALL {self.name}"

    def accept(self, visitor):
        visitor.visit_call(self)


class SlideTo(Instruction):
    def __init__(self, tantacule):
        self.tantacule = tantacule

    def __repr__(self):
        return f"SLIDETO {self.tantacule}"

    def accept(self, visitor):
        visitor.visit_slideto(self)

class SlideBack(Instruction):
    def __init__(self):
        pass

    def __repr__(self):
        return f"SLIDEBACK"

    def accept(self, visitor):
        visitor.visit_slideback(self)

class Mark(Instruction):
    def __init__(self, index):
        self.cost = 1
        self.index = index

    def __repr__(self):
        return f"MARK {self.index}"

    def accept(self, visitor):
        visitor.visit_mark(self)

class Unmark(Instruction):
    def __init__(self, index):
        self.cost = 1
        self.index = index

    def __repr__(self):
        return f"UNMARK {self.index}"

    def accept(self, visitor):
        visitor.visit_unmark(self)

class PickUp(Instruction):
    def __init__(self, handler):
        self.cost = 5
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "PICKUP"
        else:
            return f"PICKUP else {self.handler}"

    def accept(self, visitor):
        visitor.visit_pickup(self)

class Drop(Instruction):
    def __init__(self):
        self.cost = 5

    def __repr__(self):
        return "DROP"

    def accept(self, visitor):
        visitor.visit_drop(self)

class Turn(Instruction):
    def __init__(self, direction):
        self.cost = 1
        self.direction = direction

    def __repr__(self):
        return f"TURN {self.direction}"

    def accept(self, visitor):
        visitor.visit_turn(self)

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

    def accept(self, visitor):
        visitor.visit_move(self)

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

    def accept(self, visitor):
        visitor.visit_dig(self)

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

    def accept(self, visitor):
        visitor.visit_fill(self)

class Grab(Instruction):
    def __init__(self, handler):
        self.cost = 50
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "GRAB"
        else:
            return f"GRAB else {self.handler}"

    def accept(self, visitor):
        visitor.visit_grab(self)

class Attack(Instruction):
    def __init__(self, handler):
        self.cost = 30
        self.handler = handler

    def __repr__(self):
        if self.handler is None:
            return "ATTACK"
        else:
            return f"ATTACK else {self.handler}"

    def accept(self, visitor):
        visitor.visit_attack(self)
