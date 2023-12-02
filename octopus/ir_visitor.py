from octopus.ir import *

class AstVisitor():
    def visit(self, o):
        o.accept(self)

    def visit_ir(self, ir: IR):
        for bloc in ir.blocs:
            self.visit(bloc)
    
    def visit_bloc(self, bloc:Bloc):
        for instruction in bloc.instructions:
            self.visit(instruction)

    def visit_asm_instruction(self, instruction):
        pass

    def visit_asm_terminator(self, terminator):
        pass

    def visit_asm_sense(self, sense):
        pass
    
    def visit_asm_mark(self, mark):
        pass
    def visit_asm_unmark(self, unmark):
        pass
    def visit_asm_pickup(self, pickup):
        pass
    def visit_asm_drop(self, drop):
        pass
    def visit_asm_turn_left(self, turn_left):
        pass
    def visit_asm_turn_right(self, turn_right):
        pass
    def visit_asm_move(self, move):
        pass
    def visit_asm_move_up(self, move_up):
        pass
    def visit_asm_move_down(self, move_down):
        pass
    def visit_asm_dig(self, dig):
        pass
    def visit_asm_fill(self, fill):
        pass
    def visit_asm_dig_up(self, dig_up):
        pass
    def visit_asm_dig_down(self, dig_down):
        pass
    def visit_asm_fill_up(self, fill_up):
        pass
    def visit_asm_fill_down(self, fill_down):
        pass
    def visit_asm_grab(self, grab):
        pass
    def visit_asm_attack(self, attack):
        pass
    def visit_asm_roll(self, roll):
        pass
    def visit_asm_goto(self, goto):
        pass
    