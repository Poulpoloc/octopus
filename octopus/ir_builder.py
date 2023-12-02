from octopus.ast_visitor import AstVisitor
import octopus.lang_ast as ast
import octopus.ir as ir
from octopus.compiler_report import CompilerReport, CRError

ir_report = CompilerReport()

class IRBuilderVisitor(AstVisitor):
    def __init__(self):
        self.ir = ir.IR()
        self.current_bloc = None

        self.current_tantacule = None
        self.bloc_then = None
        self.bloc_else = None
        self.tantacules = {}
        self.tant_entry = {}

    def new_bloc(self):
       b = ir.Bloc()
       self.ir.add_bloc(b)
       return b

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

    def get_integer(self, index):
        if isinstance(index, ast.Number):
            return index.value
        else:
            return self.tantacules[index.name].value

    def smell(self, smell):
        match smell:
            case ast.Marker(index=index):
                return f"Marker {self.get_integer(index)}"
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
        for tantacule in program.declarations:
            if isinstance(tantacule, ast.Tantacule):
                self.tant_entry[tantacule.name] = self.new_bloc()

        if "main" not in program.tantacules:
            ir_report.error(CRError("No tantacule main", None))
            return
        self.visit(program.tantacules["main"])
        for declaration in program.declarations:
            if declaration.name != "main":
                self.visit(declaration)

    # DECLARATION
    def visit_tantacule(self, tantacule):
        self.current_bloc = self.tant_entry[tantacule.name]
        self.current_tantacule = self.current_bloc

        if tantacule.name == "main":
            self.ir.set_main_bloc(self.current_bloc)

        for instruction in tantacule.instructions:
            self.visit(instruction)
        self.current_bloc.add_terminator(ir.AsmGoto(self.tant_entry[tantacule.name]))

    def visit_macro(self, macro):
        pass

    def visit_bool(self, bool_):
        pass

    def visit_int(self, int_):
        pass

    # CONDITION
    def visit_condvar(self, condvar):
        if condvar.name not in self.tantacules:
            return
        self.visit(self.tantacules[condvar.name].condition)

    def visit_sense(self, sense):
        if isinstance(sense.smell, ast.Marker):
            sense.smell.index = self.get_integer(sense.smell.index)
        i = ir.AsmSense(sense.sense_dir, self.bloc_then, self.bloc_else, sense.smell)
        self.current_bloc.add_terminator(i)

    def visit_rand(self, rand):
        i = ir.AsmRoll(self.get_integer(rand.faces_count), self.bloc_then, self.bloc_else)
        self.current_bloc.add_terminator(i)

    def visit_not(self, not_):
        self.bloc_then, self.bloc_else = self.bloc_else, self.bloc_then
        self.visit(not_.condition)
        self.bloc_then, self.bloc_else = self.bloc_else, self.bloc_then

    def visit_or(self, or_):
        bloc_else1 = self.new_bloc()
        else_ = self.bloc_else
        self.bloc_else = bloc_else1
        self.visit(or_.left)
        self.current_bloc = bloc_else1
        self.bloc_else = else_
        self.visit(or_.right)

    def visit_and(self, and_):
        bloc_then1 = self.new_bloc()
        then = self.bloc_then
        self.bloc_then = bloc_then1
        self.visit(and_.left)
        self.current_bloc = bloc_then1
        self.bloc_then = then
        self.visit(and_.right)

    # INSTRUCTION
    def visit_repeat(self, repeat):
        for i in range(self.get_integer(repeat.number)):
            for instruction in repeat.instructions:
                self.visit(instruction)

    def visit_ifthenelse(self, ifthenelse):
        target = self.new_bloc()
        then = self.new_bloc()
        else_ = self.new_bloc()
        self.bloc_then = then
        self.bloc_else = else_

        self.visit(ifthenelse.condition)

        self.current_bloc = then
        for instruction in ifthenelse.then:
            self.visit(instruction)
        self.current_bloc.add_terminator(ir.AsmGoto(target))

        self.current_bloc = else_
        for instruction in ifthenelse.else_:
            self.visit(instruction)
        self.current_bloc.add_terminator(ir.AsmGoto(target))

        self.current_bloc = target

    def visit_while(self, while_):
        target = self.new_bloc()
        cond = self.new_bloc()
        body = self.new_bloc()
        self.current_bloc.add_terminator(ir.AsmGoto(cond))

        self.current_bloc = cond
        self.bloc_then = body
        self.bloc_else = target
        self.visit(while_.condition)

        self.current_bloc = body
        for instruction in while_.instructions:
            self.visit(instruction)
        self.current_bloc.add_terminator(ir.AsmGoto(cond))

        self.current_bloc = target

    def visit_roll(self, roll):
        roll.cases_count = self.get_integer(roll.cases_count)
        if len(roll.cases) != roll.cases_count:
            return

        if roll.cases_count == 1:
            for instruction in roll.cases[0]:
                self.visit(instruction)
            return

        if roll.cases_count % 2 == 1:
            ast.IfThenElse(ast.Rand(roll.cases_count), roll.cases[0],
                           [ast.Roll(roll.cases_count - 1, roll.cases[1:])]).accept(self)
        else:
            ast.IfThenElse(ast.Rand(2),
                           [ast.Roll(roll.cases_count // 2, roll.cases[::2])],
                           [ast.Roll(roll.cases_count // 2, roll.cases[1::2])]).accept(self)


    def visit_call(self, call):
        if call.name not in self.tantacules:
            error = CRError("Undefined macro.", call.location_span)
            ir_report.error(error)
            return
        save_map = self.tantacules
        for arg_decl, arg_value in zip(self.tantacules[call.name].args, call.args):
            arg_type, arg_name = arg_decl
            if arg_type == "bool":
                self.tantacules[arg_name] = ast.ConstBool(arg_name, arg_value)
            else:
                self.tantacules[arg_name] = ast.ConstInt(arg_name, arg_value)
        for instruction in self.tantacules[call.name].instructions:
            self.visit(instruction)
        self.tantacules = save_map


    def visit_slideto(self, slideto):
        self.current_bloc.add_terminator(ir.AsmGoto(self.tant_entry[slideto.tantacule]))

    def visit_slideback(self, slideback):
        self.current_bloc.add_terminator(ir.AsmGoto(self.current_tantacule))

    def visit_mark(self, mark):
        self.current_bloc.add_instruction(ir.AsmMark(self.get_integer(mark.index)))

    def visit_unmark(self, mark):
        self.current_bloc.add_instruction(ir.AsmUnmark(self.get_integer(mark.index)))

    def visit_pickup(self, pickup):
        follower = self.new_bloc()
        i = ir.AsmPickup(follower, None)
        b = self.current_bloc
        if pickup.handler is None:
            i.handler = follower
        else:
            i.handler = self.new_bloc()
            self.current_bloc = i.handler
            for instruction in pickup.handler:
                self.visit(instruction)
            self.current_bloc.add_instruction(ir.AsmGoto(follower))
        b.add_terminator(i)
        self.current_bloc = follower

    def visit_drop(self, drop):
        self.current_bloc.add_instruction(ir.AsmDrop())

    def visit_turn(self, turn):
        match turn.direction:
            case ast.Direction.LEFT:
                self.current_bloc.add_instruction(ir.AsmTurnLeft())
            case ast.Direction.RIGHT:
                self.current_bloc.add_instruction(ir.AsmTurnRight())

    def visit_move(self, move):
        b = self.current_bloc
        follower = self.new_bloc()
        if move.move_dir == ast.MoveDir.FORWARD:
            i = ir.AsmMove(follower, None)
        if move.move_dir == ast.MoveDir.UP:
            i = ir.AsmMoveUp(follower, None)
        if move.move_dir == ast.MoveDir.DOWN:
            i = ir.AsmMoveDown(follower, None)

        if move.handler is None:
            i.handler = follower
        else:
            i.handler = self.new_bloc()
            self.current_bloc = i.handler
            for instruction in move.handler:
                self.visit(instruction)
            self.current_bloc.add_terminator(ir.AsmGoto(follower))
        b.add_terminator(i)
        self.current_bloc = follower


    def visit_dig(self, dig):
        b = self.current_bloc
        follower = self.new_bloc()
        if dig.move_dir == ast.MoveDir.FORWARD:
            i = ir.AsmDig(follower, None)
        if dig.move_dir == ast.MoveDir.UP:
            i = ir.AsmDigUp(follower, None)
        if dig.move_dir == ast.MoveDir.DOWN:
            i = ir.AsmDigDown(follower, None)

        if dig.handler is None:
            i.handler = follower
        else:
            i.handler = self.new_bloc()
            self.current_bloc = i.handler
            for instruction in dig.handler:
                self.visit(instruction)
            self.current_bloc.add_terminator(ir.AsmGoto(follower))
        b.add_terminator(i)
        self.current_bloc = follower

    def visit_fill(self, fill):
        b = self.current_bloc
        follower = self.new_bloc()
        if fill.move_dir == ast.MoveDir.FORWARD:
            i = ir.AsmFill(follower, None)
        if fill.move_dir == ast.MoveDir.UP:
            i = ir.AsmFillUp(follower, None)
        if fill.move_dir == ast.MoveDir.DOWN:
            i = ir.AsmFillDown(follower, None)

        if fill.handler is None:
            i.handler = follower
        else:
            i.handler = self.new_bloc()
            self.current_bloc = i.handler
            for instruction in fill.handler:
                self.visit(instruction)
            self.current_bloc.add_terminator(ir.AsmGoto(follower))
        b.add_terminator(i)
        self.current_bloc = follower

    def visit_grab(self, grab):
        follower = self.new_bloc()
        i = ir.AsmGrab(follower, None)
        b = self.current_bloc
        if grab.handler is None:
            i.handler = follower
        else:
            i.handler = self.new_bloc()
            self.current_bloc = i.handler
            for instruction in grab.handler:
                self.visit(instruction)
            self.current_bloc.add_instruction(ir.AsmGoto(follower))
        b.add_terminator(i)
        self.current_bloc = follower

    def visit_attack(self, attack):
        follower = self.new_bloc()
        i = ir.AsmAttack(follower, None)
        b = self.current_bloc
        if attack.handler is None:
            i.handler = follower
        else:
            i.handler = self.new_bloc()
            self.current_bloc = i.handler
            for instruction in attack.handler:
                self.visit(instruction)
            self.current_bloc.add_instruction(ir.AsmGoto(follower))
        b.add_terminator(i)
        self.current_bloc = follower
