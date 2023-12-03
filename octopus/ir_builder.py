from octopus.ast_visitor import AstVisitor
import octopus.lang_ast as ast
import octopus.ir as ir
from octopus.compiler_report import CompilerReport, CRError

ir_report = CompilerReport()

class IRBuilderVisitor(AstVisitor):
    def __init__(self):
        self.ir = ir.IR()

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

    def get_integer(self, index, assign = None):
        if isinstance(index, ast.Number):
            return index.value
        if isinstance(index, int):
            return index
        else:
            if assign and index.name in assign:
                return assign[index.name]
            if index.name in self.tantacules:
                return self.get_integer(self.tantacules[index.name].value, assign=assign)
            return None


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
    def create_bloc_structure(self, variables):
        if len(variables) == 1:
            return [self.new_bloc() for i in range(variables[0])]
        else:
            return [self.create_bloc_structure(variables[1:]) for i in range(variables[0])]

    def new_bloc_structure(self):
        return self.create_bloc_structure(list(self.variables.values()))

    def fix_variable(self, name, value):
        follower = self.new_bloc_structure()
        backup_maxvalue = self.variables[name]

        old_var = self.variables.copy()
        new_var = self.variables.copy()
        del new_var[name]

        bs = self.create_bloc_structure(list(new_var.values()))
        k = 0
        for (assg, bloc) in self.iter_variables():
            print(self.variables, assg, k, bloc)
            k+=1
            if assg[name] != value:
                i = ir.AsmGoto(self.lookup(assg, follower))
                bloc.add_terminator(i)
            else:
                tmp = assg[name]
                del assg[name]
                self.variables = new_var
                i = ir.AsmGoto(self.lookup(assg, bs))
                self.variables = old_var
                print(self.variables)
                bloc.add_terminator(i)
                assg[name] = tmp
        self.bloc_structure = bs
        self.tantacules[name] = ast.ConstInt(name, value)
        return name, value, backup_maxvalue, follower

    def restore_backup(self, backup):
        name, value, backup_maxvalue, follower = backup
        for (asg, bloc) in self.iter_variables():
            asg[name] = value
            i = ir.AsmGoto(self.lookup(asg, follower))
            bloc.add_terminator(i)
        del self.tantacules[name]
        self.variables[name] = backup_maxvalue
        self.bloc_structure = follower


    def iter_variables_aux(self, l, depth = 0, var = {}):
        selfvars = self.variables
        print("sf", selfvars)
        for i, e in enumerate(l):
            var[list(selfvars.keys())[depth]] = i
            if isinstance(e, list):
                # Plus de variables
                yield from self.iter_variables_aux(e, depth = depth + 1, var = var)
            else:
                yield var, e
    def iter_variables(self):
        return self.iter_variables_aux(self.bloc_structure, depth = 0, var = {})

    def lookup(self, assignation, bloc_structure):
        for assg, bloc in self.iter_variables_aux(bloc_structure, var = {}):
            if assg == assignation:
                return bloc

    def visit_program(self, program):
        self.tantacules = program.tantacules
        self.variables = {}
        for tantacule in program.declarations:
            if isinstance(tantacule, ast.Variable):
                self.variables[tantacule.name] = self.get_integer(tantacule.max_value)
                del self.tantacules[tantacule.name]
            if isinstance(tantacule, ast.Tantacule):
                self.tant_entry[tantacule.name] = self.new_bloc_structure()

        # Nombre de blocs à compiler par instruction
        variables_size = 1
        for max_value in self.variables.values():
            variables_size *= max_value


        if "main" not in program.tantacules:
            ir_report.error(CRError("No tantacule main", None))
            return
        self.visit(program.tantacules["main"])
        for declaration in program.declarations:
            if declaration.name != "main":
                self.visit(declaration)

    # DECLARATION
    def visit_tantacule(self, tantacule):
        self.bloc_structure = self.tant_entry[tantacule.name]
        self.current_tantacule = self.bloc_structure

        if tantacule.name == "main":
            for _, bloc in self.iter_variables():
                self.ir.set_main_bloc(bloc)
                break

        for instruction in tantacule.instructions:
            self.visit(instruction)

        for (_, bloc), (_, first) in zip(self.iter_variables(), self.iter_variables_aux(self.tant_entry[tantacule.name], var={})):
            bloc.add_terminator(ir.AsmGoto(first))

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
        for (assign, bloc), (_, then), (_, else_) in zip(
                self.iter_variables(),
                self.iter_variables_aux(self.bloc_then, var = {}),
                self.iter_variables_aux(self.bloc_else, var = {})):
            if isinstance(sense.smell, ast.Marker):
                sense.smell.index = self.get_integer(sense.smell.index, assign = assign)
            i = ir.AsmSense(sense.sense_dir, then, else_, sense.smell)
            bloc.add_terminator(i)

    def visit_rand(self, rand):
        for (assign, bloc), (_, then), (_, else_) in zip(
                self.iter_variables(),
                self.iter_variables_aux(self.bloc_then, var = {}),
                self.iter_variables_aux(self.bloc_else, var = {})):
            i = ir.AsmRoll(self.get_integer(rand.faces_count, assign), then, else_)
            bloc.add_terminator(i)

    def visit_not(self, not_):
        self.bloc_then, self.bloc_else = self.bloc_else, self.bloc_then
        self.visit(not_.condition)
        self.bloc_then, self.bloc_else = self.bloc_else, self.bloc_then

    def visit_or(self, or_):
        bloc_else1 = self.new_bloc_structure()
        elses = self.bloc_else

        self.bloc_else = bloc_else1
        self.visit(or_.left)
        self.bloc_structure = bloc_else1
        self.bloc_else = elses
        self.visit(or_.right)

    def visit_and(self, and_):
        bloc_then1 = self.new_bloc_structure()
        thens = self.bloc_then

        self.bloc_then = bloc_then1
        self.visit(and_.left)
        self.bloc_structure = bloc_then1
        self.bloc_then = thens
        self.visit(and_.right)

    # INSTRUCTION
    def visit_assign(self, assign):
        followers = self.new_bloc_structure()
        for (ass, bloc) in self.iter_variables():
            value = self.get_integer(assign.value, assign=ass)
            ass[assign.name] = value
            i = ir.AsmGoto(self.lookup(ass, followers))
            bloc.add_terminator(i)
        self.bloc_structure=followers

    def visit_repeat(self, repeat):
        if self.get_integer(repeat.number) is None:
            var = repeat.number.name
            for value in range(self.variables[var]):
                backup = self.fix_variable(var, value)
                for i in range(self.get_integer(repeat.number)):
                    for instruction in repeat.instructions:
                        self.visit(instruction)
                self.restore_backup(backup)
        else:
            for i in range(self.get_integer(repeat.number)):
                for instruction in repeat.instructions:
                    self.visit(instruction)

    def visit_case(self, case_):
        var = case_.name
        for value, instructions in enumerate(case_.cases):
            backup = self.fix_variable(var, value)
            for instruction in instructions:
                self.visit(instruction)
            self.restore_backup(backup)

    def visit_ifthenelse(self, ifthenelse):
        targets = self.new_bloc_structure()
        thens = self.new_bloc_structure()
        elses = self.new_bloc_structure()
        self.bloc_then = thens
        self.bloc_else = elses

        self.visit(ifthenelse.condition)

        self.bloc_structure = thens
        for instruction in ifthenelse.then:
            self.visit(instruction)
        for (_, bloc), (_, target) in zip(self.iter_variables(), self.iter_variables_aux(targets, var = {})):
            bloc.add_terminator(ir.AsmGoto(target))

        self.bloc_structure = elses
        for instruction in ifthenelse.else_:
            self.visit(instruction)
        for (_, bloc), (_, target) in zip(self.iter_variables(), self.iter_variables_aux(targets, var = {})):
            bloc.add_terminator(ir.AsmGoto(target))

        self.bloc_structure = targets

    def visit_while(self, while_):
        targets = self.new_bloc_structure()
        conds = self.new_bloc_structure()
        bodys = self.new_bloc_structure()

        for (_, bloc), (_, cond) in zip(self.iter_variables(), self.iter_variables_aux(conds, var = {})):
            bloc.add_terminator(ir.AsmGoto(cond))

        self.bloc_structure = conds
        self.bloc_then = bodys
        self.bloc_else = targets
        self.visit(while_.condition)

        self.bloc_structure = bodys
        for instruction in while_.instructions:
            self.visit(instruction)
        for (_, bloc), (_, cond) in zip(self.iter_variables(), self.iter_variables_aux(conds, var = {})):
            bloc.add_terminator(ir.AsmGoto(cond))

        self.bloc_structure = targets

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
        for (_, bloc), (_, target) in zip(self.iter_variables(), self.iter_variables_aux(self.tant_entry[slideto.tantacule], var = {})):
            bloc.add_terminator(ir.AsmGoto(target))

    def visit_slideback(self, slideback):
        for (_, bloc), (_, target) in zip(self.iter_variables(), self.iter_variables_aux(self.current_tantacule, var = {})):
            bloc.add_terminator(ir.AsmGoto(target))

    def visit_mark(self, mark):
        for assign, bloc in self.iter_variables():
            bloc.add_instruction(ir.AsmMark(self.get_integer(mark.index, assign=assign)))

    def visit_unmark(self, mark):
        for assign, bloc in self.iter_variables():
            bloc.add_instruction(ir.AsmUnmark(self.get_integer(mark.index, assign=assign)))

    def visit_pickup(self, pickup):
        followers = self.new_bloc_structure()
        handlers = None

        if pickup.handler is not None:
            handlers = self.new_bloc_structure()
            old_bloc_structure =  self.bloc_structure
            self.bloc_structure = handlers
            for instruction in pickup.handler:
                self.visit(instruction)
            for (_, bloc), (_, follower) in zip(self.iter_variables(), self.iter_variables_aux(followers, var = {})):
                bloc.add_terminator(ir.AsmGoto(follower))
            self.bloc_structure = old_bloc_structure
        else:
            handlers = followers


        for (assign, bloc), (_, handler), (_, follower) in zip(self.iter_variables(),
                                                               self.iter_variables_aux(handlers, var = {}),
                                                               self.iter_variables_aux(followers, var = {})):
            bloc.add_terminator(ir.AsmPickup(follower, handler))
        self.bloc_structure = followers

    def visit_drop(self, drop):
        for (_, bloc) in self.iter_variables():
            bloc.add_instruction(ir.AsmDrop())

    def visit_turn(self, turn):
        for (_, bloc) in self.iter_variables():
            match turn.direction:
                case ast.Direction.LEFT:
                    bloc.add_instruction(ir.AsmTurnLeft())
                case ast.Direction.RIGHT:
                    bloc.add_instruction(ir.AsmTurnRight())

    def visit_move(self, move):
        followers = self.new_bloc_structure()
        handlers = None

        if move.handler is not None:
            handlers = self.new_bloc_structure()
            old_bloc_structure =  self.bloc_structure
            self.bloc_structure = handlers
            for instruction in move.handler:
                self.visit(instruction)
            for (_, bloc), (_, follower) in zip(self.iter_variables(), self.iter_variables_aux(followers, var = {})):
                bloc.add_instruction(ir.AsmGoto(follower))
            self.bloc_structure = old_bloc_structure
        else:
            handlers = followers


        for (assign, bloc), (_, handler), (_, follower) in zip(self.iter_variables(),
                                                               self.iter_variables_aux(handlers, var = {}),
                                                               self.iter_variables_aux(followers, var = {})):
            i = None
            if move.move_dir == ast.MoveDir.FORWARD:
                i = ir.AsmMove(follower, handler)
            if move.move_dir == ast.MoveDir.UP:
                i = ir.AsmMoveUp(follower, handler)
            if move.move_dir == ast.MoveDir.DOWN:
                i = ir.AsmMoveDown(follower, handler)
            bloc.add_terminator(i)
        self.bloc_structure = followers

    def visit_dig(self, dig):
        followers = self.new_bloc_structure()
        handlers = None

        if dig.handler is not None:
            handlers = self.new_bloc_structure()
            old_bloc_structure =  self.bloc_structure
            self.bloc_structure = handlers
            for instruction in dig.handler:
                self.visit(instruction)
            for (_, bloc), (_, follower) in zip(self.iter_variables(), self.iter_variables_aux(followers, var = {})):
                bloc.add_instruction(ir.AsmGoto(follower))
            self.bloc_structure = old_bloc_structure
        else:
            handlers = followers


        for (assign, bloc), (_, handler), (_, follower) in zip(self.iter_variables(),
                                                               self.iter_variables_aux(handlers, var = {}),
                                                               self.iter_variables_aux(followers, var = {})):
            i = None
            if dig.move_dir == ast.MoveDir.FORWARD:
                i = ir.AsmDig(follower, handler)
            if dig.move_dir == ast.MoveDir.UP:
                i = ir.AsmDigUp(follower, handler)
            if dig.move_dir == ast.MoveDir.DOWN:
                i = ir.AsmDigDown(follower, handler)
            bloc.add_terminator(i)
        self.bloc_structure = followers

    def visit_fill(self, fill):
        followers = self.new_bloc_structure()
        handlers = None

        if fill.handler is not None:
            handlers = self.new_bloc_structure()
            old_bloc_structure =  self.bloc_structure
            self.bloc_structure = handlers
            for instruction in fill.handler:
                self.visit(instruction)
            for (_, bloc), (_, follower) in zip(self.iter_variables(), self.iter_variables_aux(followers, var = {})):
                bloc.add_instruction(ir.AsmGoto(follower))
            self.bloc_structure = old_bloc_structure
        else:
            handlers = followers


        for (assign, bloc), (_, handler), (_, follower) in zip(self.iter_variables(),
                                                               self.iter_variables_aux(handlers, var = {}),
                                                               self.iter_variables_aux(followers, var = {})):
            i = None
            if fill.move_dir == ast.MoveDir.FORWARD:
                i = ir.AsmFill(follower, handler)
            if fill.move_dir == ast.MoveDir.UP:
                i = ir.AsmFillUp(follower, handler)
            if fill.move_dir == ast.MoveDir.DOWN:
                i = ir.AsmFillDown(follower, handler)
            bloc.add_terminator(i)
        self.bloc_structure = followers

    def visit_grab(self, grab):
        followers = self.new_bloc_structure()
        handlers = None

        if grab.handler is not None:
            handlers = self.new_bloc_structure()
            old_bloc_structure =  self.bloc_structure
            self.bloc_structure = handlers
            for instruction in grab.handler:
                self.visit(instruction)
            for (_, bloc), (_, follower) in zip(self.iter_variables(), self.iter_variables_aux(followers, var = {})):
                bloc.add_terminator(ir.AsmGoto(follower))
            self.bloc_structure = old_bloc_structure
        else:
            handlers = followers


        for (assign, bloc), (_, handler), (_, follower) in zip(self.iter_variables(),
                                                               self.iter_variables_aux(handlers, var = {}),
                                                               self.iter_variables_aux(followers, var = {})):
            bloc.add_terminator(ir.AsmGrab(follower, handler))
        self.bloc_structure = followers

    def visit_attack(self, attack):
        followers = self.new_bloc_structure()
        handlers = None

        if attack.handler is not None:
            handlers = self.new_bloc_structure()
            old_bloc_structure =  self.bloc_structure
            self.bloc_structure = handlers
            for instruction in attack.handler:
                self.visit(instruction)
            for (_, bloc), (_, follower) in zip(self.iter_variables(), self.iter_variables_aux(followers, var = {})):
                bloc.add_terminator(ir.AsmGoto(follower))
            self.bloc_structure = old_bloc_structure
        else:
            handlers = followers


        for (assign, bloc), (_, handler), (_, follower) in zip(self.iter_variables(),
                                                               self.iter_variables_aux(handlers, var = {}),
                                                               self.iter_variables_aux(followers, var = {})):
            bloc.add_terminator(ir.AsmAttack(follower, handler))
        self.bloc_structure = followers
