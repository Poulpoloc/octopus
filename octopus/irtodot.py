from octopus.ir_visitor import IRVisitor
from octopus.ir import *

class IRDotGenerator(IRVisitor):
    def __init__(self):
        self.output = ""
        self.link = ""
    
    def generate(self, inp : IR):
        self.output = """digraph structs {
    node [shape=record];
"""
        self.link = ""
        self.visit(inp)
        self.output += self.link
        self.output += "}"
        return self.output
    
    def visit_ir(self, ir: IR):
        self.main_block = ir.main_bloc
        for bloc in ir.blocs:
            self.visit(bloc)
    
    def visit_bloc(self, bloc: Bloc):
        self.current_bloc : Bloc = bloc
        if bloc == self.main_block:
            self.output += f"    {bloc.identifier} [penwidth={(len(bloc.predecessors)//3)+1},color=blue, label=\"{'{'}\n"
        else:
            self.output += f"    {bloc.identifier} [penwidth={(len(bloc.predecessors)//3)+1},label=\"{'{'}\n"
        for instruction in bloc.instructions:
            self.visit(instruction)
        self.output += "    }}\"];\n"
    
    def visit_asm_sense(self, sense : AsmSense):
        self.output += "        |{Sense\n"
        for succ in sense.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"

    def visit_asm_mark(self, mark : AsmMark):
        self.output += f"        Mark {mark.index}\\n\n"

    def visit_asm_unmark(self, unmark : AsmUnmark):
        self.output += f"        UnMark {unmark.index}\\n\n"

    def visit_asm_pickup(self, pickup : AsmPickup):
        self.output += "        |{Pickup\n"
        for succ in pickup.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"

    def visit_asm_drop(self, drop):
        self.output += "        Drop\\n\n"

    def visit_asm_turn_left(self, turn_left:AsmTurnLeft):
        self.output += "        Turn Left\\n\n"

    def visit_asm_turn_right(self, turn_right:AsmTurnRight):
        self.output += "        Turn Right\\n\n"

    def visit_asm_move(self, move : AsmMove):
        self.output += "        |{Move\n"
        for succ in move.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"

    def visit_asm_move_up(self, move_up):
        self.output += "        |{Move Up\n"
        for succ in move_up.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_move_down(self, move_down):
        self.output += "        |{Move Down\n"
        for succ in move_down.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_dig(self, dig):
        self.output += "        |{Dig\n"
        for succ in dig.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_fill(self, fill):
        self.output += "        |{Fill\n"
        for succ in fill.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_dig_up(self, dig_up):
        self.output += "        |{Dig Up\n"
        for succ in dig_up.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_dig_down(self, dig_down):
        self.output += "        |{Dig Down\n"
        for succ in dig_down.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_fill_up(self, fill_up):
        self.output += "        |{Fill Up\n"
        for succ in fill_up.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_fill_down(self, fill_down):
        self.output += "        |{Fill Down\n"
        for succ in fill_down.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_grab(self, grab):
        self.output += "        |{Grab\n"
        for succ in grab.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_attack(self, attack):
        self.output += "        |{Attack\n"
        for succ in attack.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_roll(self, roll):
        self.output += "        |{Roll\n"
        for succ in roll.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"
    def visit_asm_goto(self, goto):
        self.output += "        |{Goto\n"
        for succ in goto.get_successors():
            self.link +=f"   {self.current_bloc.identifier} -> {succ.identifier};\n"