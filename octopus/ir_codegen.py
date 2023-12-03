from octopus.ir_visitor import IRVisitor
import octopus.lang_ast as ast

class StringBuilder:
    def __init__(self):
        self.strings = []

    def append(self, string):
        self.strings.append(string)

    def to_string(self):
        return '\n'.join(self.strings)

def label(bloc):
    return f"l{bloc.identifier}"

def move_dir(move_dir):
    match move_dir:
        case ast.MoveDir.FORWARD:
            return ""
        case ast.MoveDir.UP:
            return "Up"
        case ast.MoveDir.DOWN:
            return "Down"

def sense_dir(sense_dir):
    match sense_dir:
        case ast.SenseDir.HERE:
            return "Here"
        case ast.SenseDir.AHEAD:
            return "Ahead"
        case ast.SenseDir.LEFTAHEAD:
            return "LeftAhead"
        case ast.SenseDir.RIGHTAHEAD:
            return "RightAhead"
        case ast.SenseDir.ABOVE:
            return "Above"
        case ast.SenseDir.BELOW:
            return "Below"

def smell(smell):
    match smell:
        case ast.Marker(index=index):
            return f"Marker {index}"
        case ast.AtomicSmell.FRIEND:
            return "Friend"
        case ast.AtomicSmell.ENEMY:
            return "Enemy"
        case ast.AtomicSmell.GRABBED:
            return "Grabbed"
        case ast.AtomicSmell.FRIENDWITHFOOD:
            return "FriendWithFOOD"
        case ast.AtomicSmell.ENEMYWITHFOOD:
            return "EnemyWithFood"
        case ast.AtomicSmell.FOOD:
            return "Food"
        case ast.AtomicSmell.ROCK:
            return "Rock"
        case ast.AtomicSmell.EMPTY:
            return "Empty"
        case ast.AtomicSmell.UNDERGROUND:
            return "Underground"
        case ast.AtomicSmell.SURFACE:
            return "Surface"
        case ast.AtomicSmell.HOLEABOVE:
            return "HoleAbove"
        case ast.AtomicSmell.HOLEBELOW:
            return "HoleBelow"
        case ast.AtomicSmell.ENEMYMARKER:
            return "EnemyMarker"
        case ast.AtomicSmell.HOME:
            return "Home "
        case ast.AtomicSmell.ENEMYHOME:
            return "EnemyHome"

class IRCodeGenerator(IRVisitor):
    def __init__(self):
        self.code = StringBuilder()
        self.visited = set()

    def visit_ir(self, ir):
        self.visit(ir.main_bloc)
        print(ir.main_bloc)
        for bloc in ir.blocs:
            if bloc not in self.visited:
                self.visit(bloc)

    def visit_bloc(self, bloc):
        self.visited.add(bloc)
        self.code.append(f"{label(bloc)}:")
        for asm_instruction in bloc.instructions:
            self.visit(asm_instruction)

    def visit_asm_sense(self, sense):
        self.code.append(
            f"Sense {sense_dir(sense.direction)} {label(sense.then)} {label(sense.else_)} {smell(sense.condition)}"
        )

    def visit_asm_mark(self, mark):
        self.code.append(f"Mark {mark.index}")

    def visit_asm_unmark(self, unmark):
        self.code.append(f"Unmark {unmark.index}")

    def visit_asm_pickup(self, pickup):
        self.code.append(f"PickUp {label(pickup.handler)}")
        if pickup.follower not in self.visited:
            self.visit(pickup.follower)
        else:
            self.code.append(f"Goto {label(pickup.follower)}")

    def visit_asm_drop(self, drop):
        self.code.append(f"Drop")

    def visit_asm_turn_left(self, turn_left):
        self.code.append(f"TurnLeft")

    def visit_asm_turn_right(self, turn_right):
        self.code.append(f"TurnRight")

    def visit_asm_move(self, move):
        self.code.append(f"Move {label(move.handler)}")
        if move.follower not in self.visited:
            self.visit(move.follower)
        else:
            self.code.append(f"Goto {label(move.follower)}")

    def visit_asm_move_up(self, move_up):
        self.code.append(f"MoveUp {label(move_up.handler)}")
        if move_up.follower not in self.visited:
            self.visit(move_up.follower)
        else:
            self.code.append(f"Goto {label(move_up.follower)}")

    def visit_asm_move_down(self, move_down):
        self.code.append(f"MoveDown {label(move_down.handler)}")
        if move_down.follower not in self.visited:
            self.visit(move_down.follower)
        else:
            self.code.append(f"Goto {label(move_down.follower)}")

    def visit_asm_dig(self, dig):
        self.code.append(f"Dig {label(dig.handler)}")
        if dig.follower not in self.visited:
            self.visit(dig.follower)
        else:
            self.code.append(f"Goto {label(dig.follower)}")

    def visit_asm_fill(self, fill):
        self.code.append(f"Fill {label(fill.handler)}")
        if fill.follower not in self.visited:
            self.visit(fill.follower)
        else:
            self.code.append(f"Goto {label(fill.follower)}")

    def visit_asm_dig_up(self, dig_up):
        self.code.append(f"DigUp {label(dig_up.handler)}")
        if dig_up.follower not in self.visited:
            self.visit(dig_up.follower)
        else:
            self.code.append(f"Goto {label(dig_up.follower)}")

    def visit_asm_dig_down(self, dig_down):
        self.code.append(f"DigDown {label(dig_down.handler)}")
        if dig_down.follower not in self.visited:
            self.visit(dig_down.follower)
        else:
            self.code.append(f"Goto {label(dig_down.follower)}")

    def visit_asm_fill_up(self, fill_up):
        self.code.append("FillUp")

    def visit_asm_fill_down(self, fill_down):
        self.code.append("FillDown")

    def visit_asm_grab(self, grab):
        self.code.append(f"Grab {label(grab.handler)}")
        if grab.follower not in self.visited:
            self.visit(grab.follower)
        else:
            self.code.append(f"Goto {label(grab.follower)}")

    def visit_asm_attack(self, attack):
        self.code.append(f"Attack {label(attack.handler)}")
        if attack.follower not in self.visited:
            self.visit(attack.follower)
        else:
            self.code.append(f"Goto {label(attack.follower)}")
        pass

    def visit_asm_roll(self, roll):
        self.code.append(
            f"Roll {roll.faces_count} {label(roll.then)} {label(roll.else_)}"
        )

    def visit_asm_goto(self, goto):
        self.code.append(f"Goto {label(goto.target)}")
