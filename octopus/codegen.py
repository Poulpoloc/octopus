from octopus.ast_visitor import AstVisitor
import octopus.lang_ast as ast
from octopus.compiler_report import CompilerReport, CRError

codegen_report = CompilerReport()

class CodeGenVisitor(AstVisitor):
    def __init__(self):
        self.label_counter = 0
        self.code = ""
        self.current_tantacule = ""
        self.label_then = ""
        self.label_else = ""
        self.tantacules = {}

    def fresh_label(self):
        self.label_counter += 1
        return f"l{self.label_counter}"

    def write_code(self, code):
        self.code = "\n".join([
            self.code,
            code,
        ])

    def get_code(self):
        return self.code

    def move_dir(self, move_dir):
        match move_dir:
            case ast.MoveDir.FORWARD:
                return ""
            case ast.MoveDir.UP:
                return "Up"
            case ast.MoveDir.DOWN:
                return "Down"

    def sense_dir(self, sense_dir):
        match sense_dir:
            case ast.SenseDir.HERE:
                return "Here"
            case ast.SenseDir.AHEAD:
                return "AHEAD"
            case ast.SenseDir.LEFTAHEAD:
                return "LEFTAHEAD"
            case ast.SenseDir.RIGHTAHEAD:
                return "RIGHTAHEAD"
            case ast.SenseDir.ABOVE:
                return "ABOVE"
            case ast.SenseDir.BELOW:
                return "BELOW"

    def smell(self, smell):
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

    # PROGRAM
    def visit_program(self, program):
        self.tantacules = program.tantacules
        if "main" not in program.tantacules:
            codegen_report.error(CRError("No tantacule main", None))
        self.visit(program.tantacules["main"])
        for declaration in program.declarations:
            if declaration.name != "main":
                self.visit(declaration)

    # DECLARATION
    def visit_tantacule(self, tantacule):
        self.current_tantacule = tantacule.name
        self.write_code(f"{tantacule.name}:")
        for instruction in tantacule.instructions:
            self.visit(instruction)
        self.write_code(f"Goto {tantacule.name}")

    def visit_macro(self, macro):
        pass

    # CONDITION
    def visit_sense(self, sense):
        dir = self.sense_dir(sense.sense_dir)
        cond = self.smell(sense.smell)
        self.write_code(f"Sense {dir} {self.label_then} {self.label_else} {cond}")

    def visit_rand(self, rand):
        self.write_code(f"Roll {rand.faces_count} {self.label_then} {self.label_else}")

    def visit_not(self, not_):
        self.label_then, self.label_else = self.label_else, self.label_then
        self.visit(not_.condition)
        self.label_then, self.label_else = self.label_else, self.label_then

    def visit_or(self, or_):
        lbl_else1 = self.fresh_label()
        else_ = self.label_else
        self.label_else = lbl_else1
        self.visit(or_.left)
        self.write_code(f"{lbl_else1}:")
        self.label_else = else_
        self.visit(or_.right)

    def visit_and(self, and_):
        lbl_then1 = self.fresh_label()
        then = self.label_then
        self.label_then = lbl_then1
        self.visit(and_.left)
        self.write_code(f"{lbl_then1}:")
        self.label_then = then
        self.visit(and_.right)

    # INSTRUCTION
    def visit_repeat(self, repeat):
        for i in range(repeat.number):
            for instruction in self.instructions:
                self.visit(instruction)

    def visit_ifthenelse(self, ifthenelse):
        self.label_then = self.fresh_label()
        self.label_else = self.fresh_label()
        label_then = self.label_then
        label_else = self.label_else
        label_out = self.fresh_label()

        self.visit(ifthenelse.condition)
        self.write_code(f"{label_then}:")
        for instruction in ifthenelse.then:
            self.visit(instruction)
        self.write_code(f"Goto {label_out}")
        self.write_code(f"{label_else}:")
        for instruction in ifthenelse.else_:
            self.visit(instruction)
        self.write_code(f"Goto {label_out}")
        self.write_code(f"{label_out}:")

    def visit_while(self, while_):
        self.label_then = self.fresh_label()
        self.label_else = self.fresh_label()
        label_then = self.label_then
        label_else = self.label_else
        label_in = self.fresh_label()

        self.write_code(f"{label_in}:")
        self.visit(while_.condition)
        self.write_code(f"{label_then}:")
        for instruction in while_.instructions:
            self.visit(instruction)
        self.write_code(f"Goto {label_in}")
        self.write_code(f"{label_else}:")

    def visit_call(self, call):
        if call.name not in self.tantacules:
            error = CRError("Undefined macro.", call.location_span)
            codegen_report.error(error)
            return
        for instruction in self.tantacules[call.name].instructions:
            self.visit(instruction)


    def visit_slideto(self, slideto):
        self.write_code(f"Goto {slideto.tantacule}")

    def visit_slideback(self, slideback):
        self.write_code(f"Goto {self.current_tantacule}")

    def visit_mark(self, mark):
        self.write_code(f"Mark {mark.index}")

    def visit_unmark(self, mark):
        self.write_code(f"Unmark {mark.index}")

    def visit_pickup(self, pickup):
        if pickup.handler is None:
            lbl = self.fresh_label()
            self.write_code(f"PickUp {lbl}")
            self.write_code(f"{lbl}:")
        else:
            lbl1 = self.fresh_label()
            lbl2 = self.fresh_label()

            self.write_code(f"Pickup {lbl2}")
            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl2}:")

            for instruction in pickup.handler:
                self.visit(instruction)

            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl1}:")

    def visit_drop(self, drop):
        self.write_code("Drop")

    def visit_turn(self, turn):
        match turn.direction:
            case ast.Direction.LEFT:
                self.write_code("TurnLeft")
            case ast.Direction.RIGHT:
                self.write_code("TurnRight")

    def visit_move(self, move):
        dir = self.move_dir(move.move_dir)
        if move.handler is None:
            lbl = self.fresh_label()
            self.write_code(f"Move{dir} {lbl}")
            self.write_code(f"{lbl}:")
        else:
            lbl1 = self.fresh_label()
            lbl2 = self.fresh_label()

            self.write_code(f"Move{dir} {lbl2}")
            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl2}:")

            for instruction in move.handler:
                self.visit(instruction)

            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl1}:")

    def visit_dig(self, dig):
        dir = self.move_dir(dig.move_dir)
        if dig.handler is None:
            lbl = self.fresh_label()
            self.write_code(f"Dig{dir} {lbl}")
            self.write_code(f"{lbl}:")
        else:
            lbl1 = self.fresh_label()
            lbl2 = self.fresh_label()

            self.write_code(f"Dig{dir} {lbl2}")
            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl2}:")

            for instruction in dig.handler:
                self.visit(instruction)

            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl1}:")

    def visit_fill(self, fill):
        dir = self.move_dir(fill.move_dir)
        if fill.handler is None:
            lbl = self.fresh_label()
            self.write_code(f"Fill{dir} {lbl}")
            self.write_code(f"{lbl}:")
        else:
            lbl1 = self.fresh_label()
            lbl2 = self.fresh_label()

            self.write_code(f"Fill{dir} {lbl2}")
            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl2}:")

            for instruction in fill.handler:
                self.visit(instruction)

            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl1}:")

    def visit_grab(self, grab):
        if grab.handler is None:
            lbl = self.fresh_label()
            self.write_code(f"Grab {lbl}")
            self.write_code(f"{lbl}:")
        else:
            lbl1 = self.fresh_label()
            lbl2 = self.fresh_label()

            self.write_code(f"Grab {lbl2}")
            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl2}:")

            for instruction in grab.handler:
                self.visit(instruction)

            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl1}:")

    def visit_attack(self, attack):
        if attack.handler is None:
            lbl = self.fresh_label()
            self.write_code(f"Attack {lbl}")
            self.write_code(f"{lbl}:")
        else:
            lbl1 = self.fresh_label()
            lbl2 = self.fresh_label()

            self.write_code(f"Attack {lbl2}")
            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl2}:")

            for instruction in attack.handler:
                self.visit(instruction)

            self.write_code(f"Goto {lbl1}")
            self.write_code(f"{lbl1}:")
