class IR:
    def __init__(self):
        self.blocs = []
        self.main_bloc = None

    def set_main_bloc(self, bloc):
        self.main_bloc = bloc


    def add_bloc(self, bloc):
        self.blocs.append(bloc)


class Bloc:
    counter = 0

    def __init__(self):
        Bloc.counter += 1
        self.identifier = Bloc.counter
        self.instructions = []
        self.predecessors = []

    def get_terminator(self):
        return self.instructions[-1]

    def add_predecessor(self, bloc):
        self.predecessors.append(bloc)

    def get_successors(self):
        self.get_terminator().get_successors()

    def is_sealed(self):
        return self.instructions != [] and isinstance(self.instructions[-1], AsmTerminator)

    def add_instruction(self, instruction):
        if not self.is_sealed():
            self.instructions.append(instruction)

    def add_terminator(self, terminator):
        if not self.is_sealed():
            self.instructions.append(terminator)
            for bloc in terminator.get_successors():
                bloc.add_predecessor(self)

class AsmInstruction:
    pass

class AsmTerminator(AsmInstruction):
    pass

class AsmSense(AsmTerminator):
    def __init__(self, direction, then, else_, condition):
        self.direction = direction
        self.then = then
        self.else_ = else_
        self.condition = condition
        self.cost = 1

    def get_successors(self):
        return [self.then, self.else_]

class AsmMark(AsmInstruction):
    def __init__(self, index):
        self.index = index
        self.cost = 1

class AsmUnmark(AsmInstruction):
    def __init__(self, index):
        self.index = index
        self.cost = 1

class AsmPickup(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost=  5

    def get_successors(self):
        return [self.follower, self.handler]

class AsmDrop(AsmInstruction):
    def __init__(self):
        self.cost = 5

class AsmTurnLeft(AsmInstruction):
    def __init__(self):
        self.cost = 1

class AsmTurnRight(AsmInstruction):
    def __init__(self):
        self.cost = 1

class AsmMove(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 20

    def get_successors(self):
        return [self.follower, self.handler]

class AsmMoveUp(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 20

    def get_successors(self):
        return [self.follower, self.handler]

class AsmMoveDown(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 20

    def get_successors(self):
        return [self.follower, self.handler]

class AsmDig(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]

class AsmFill(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]

class AsmDigUp(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]

class AsmDigDown(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]

class AsmFillUp(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]

class AsmFillDown(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]

class AsmGrab(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 50

    def get_successors(self):
        return [self.follower, self.handler]

class AsmAttack(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 30

    def get_successors(self):
        return [self.follower, self.handler]

class AsmRoll(AsmTerminator):
    def __init__(self, faces_count, then, else_):
        self.faces_count = faces_count
        self.then = then
        self.else_ = else_
        self.cost = 1

    def get_successors(self):
        return [self.then, self.else_]

class AsmGoto(AsmTerminator):
    def __init__(self, target):
        self.target = target
        self.cost = 1

    def get_successors(self):
        return [self.target]
