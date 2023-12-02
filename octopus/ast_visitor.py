class AstVisitor():
    def visit(self, o):
        o.accept(self)

    # PROGRAM
    def visit_program(self, program):
        for declaration in program.declarations:
            self.visit(declaration)

    # DECLARATION
    def visit_tantacule(self, tantacule):
        for instruction in tantacule.instructions:
            self.visit(instruction)

    # CONDITION
    def visit_sense(self, sense):
        pass

    def visit_rand(self, rand):
        pass

    def visit_not(self, not_):
        self.visit(not_.condition)

    def visit_or(self, or_):
        self.visit(or_.left)
        self.visit(or_.right)

    def visit_and(self, and_):
        self.visit(and_.left)
        self.visit(and_.right)

    # INSTRUCTION
    def visit_repeat(self, repeat):
        for instruction in self.instructions:
            self.visit(instruction)

    def visit_ifthenelse(self, ifthenelse):
        self.visit(ifthenelse.condition)
        for instruction in ifthenelse.then:
            self.visit(instruction)
        for instruction in ifthenelse.else_:
            self.visit(instruction)

    def visit_while(self, while_):
        self.visit(while_.condition)
        for instruction in while_.instructions:
            self.visit(instruction)

    def visit_slideto(self, slideto):
        pass

    def visit_slideback(self, slideback):
        pass

    def visit_mark(self, mark):
        pass

    def visit_unmark(self, mark):
        pass

    def visit_pickup(self, pickup):
        for instruction in pickup.handler:
            self.visit(instruction)

    def visit_drop(self, drop):
        pass

    def visit_turn(self, turn):
        pass

    def visit_move(self, move):
        if move.handler is not None:
            for instruction in move.handler:
                self.visit(instruction)

    def visit_dig(self, dig):
        if dig.handler is not None:
            for instruction in dig.handler:
                self.visit(instruction)

    def visit_fill(self, fill):
        if fill.handler is not None:
            for instruction in fill.handler:
                self.visit(instruction)

    def visit_grab(self, grab):
        if grab.handler is not None:
            for instruction in grab.handler:
                self.visit(grab)

    def visit_attack(self, attack):
        if attack.handler is not None:
            for instruction in attack.handler:
                self.visit(attack)
