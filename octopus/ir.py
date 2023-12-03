class IR:
    def __init__(self):
        self.blocs = []
        self.main_bloc = None

    def set_main_bloc(self, bloc):
        self.main_bloc = bloc


    def add_bloc(self, bloc):
        self.blocs.append(bloc)

    def accept(self, visitor):
        visitor.visit_ir(self)


class Bloc:
    counter = 0

    def __init__(self):
        Bloc.counter += 1
        self.identifier = Bloc.counter
        self.instructions = []
        self.predecessors : list[Bloc] = []

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
                if bloc is not None:
                    bloc.add_predecessor(self)

    def accept(self, visitor):
        visitor.visit_bloc(self)

class AsmInstruction:
    def accept(self, visitor):
        visitor.visit_asm_instruction(self)

class AsmTerminator(AsmInstruction):
    def accept(self, visitor):
        visitor.visit_asm_terminator(self)

class AsmSense(AsmTerminator):
    def __init__(self, direction, then, else_, condition):
        self.direction = direction
        self.then = then
        self.else_ = else_
        self.condition = condition
        self.cost = 1

    def get_successors(self):
        return [self.then, self.else_]
    
    def replace(self, old, new):
        if old == self.then:
            self.then = new
        elif old == self.else_:
            self.else_ = new
    
    def accept(self, visitor):
        visitor.visit_asm_sense(self)

class AsmMark(AsmInstruction):
    def __init__(self, index):
        self.index = index
        self.cost = 1

    def accept(self, visitor):
        visitor.visit_asm_mark(self)

class AsmUnmark(AsmInstruction):
    def __init__(self, index):
        self.index = index
        self.cost = 1

    def accept(self, visitor):
        visitor.visit_asm_unmark(self)

class AsmPickup(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost=  5

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_pickup(self)

class AsmDrop(AsmInstruction):
    def __init__(self):
        self.cost = 5

    def accept(self, visitor):
        visitor.visit_asm_drop(self)

class AsmTurnLeft(AsmInstruction):
    def __init__(self):
        self.cost = 1

    def accept(self, visitor):
        visitor.visit_asm_turn_left(self)

class AsmTurnRight(AsmInstruction):
    def __init__(self):
        self.cost = 1

    def accept(self, visitor):
        visitor.visit_asm_turn_right(self)

class AsmMove(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 20

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_move(self)

class AsmMoveUp(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 20

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_move_up(self)

class AsmMoveDown(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 20

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_move_down(self)

class AsmDig(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_dig(self)

class AsmFill(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_fill(self)

class AsmDigUp(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_dig_up(self)

class AsmDigDown(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_dig_down(self)

class AsmFillUp(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_fill_up(self)

class AsmFillDown(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 25

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_fill_down(self)

class AsmGrab(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 50

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_grab(self)

class AsmAttack(AsmTerminator):
    def __init__(self, follower, handler):
        self.follower = follower
        self.handler = handler
        self.cost = 30

    def get_successors(self):
        return [self.follower, self.handler]
    
    def replace(self, old, new):
        if old == self.follower:
            self.follower = new
        elif old == self.handler:
            self.handler = new
    
    def accept(self, visitor):
        visitor.visit_asm_attack(self)

class AsmRoll(AsmTerminator):
    def __init__(self, faces_count, then, else_):
        self.faces_count = faces_count
        self.then = then
        self.else_ = else_
        self.cost = 1

    def get_successors(self):
        return [self.then, self.else_]
    
    def replace(self, old, new):
        if old == self.then:
            self.then = new
        elif old == self.else_:
            self.else_ = new
    
    def accept(self, visitor):
        visitor.visit_asm_roll(self)
    

class AsmGoto(AsmTerminator):
    def __init__(self, target):
        self.target = target
        self.cost = 1

    def get_successors(self):
        return [self.target]
    
    def replace(self, old, new):
        if old == self.target:
            self.target = new
        
    def accept(self, visitor):
        visitor.visit_asm_goto(self)
