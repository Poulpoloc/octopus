from octopus.ir_visitor import IRVisitor
from octopus.ir import *



class IRGotoOptimizer(IRVisitor):

    def visit_ir(self, ir: IR):
        self.ir = ir
        for bloc in sorted(ir.blocs, key=lambda b: len(b.predecessors)):
            self.visit(bloc)


    def visit_bloc(self, bloc: Bloc):
        if(isinstance(bloc.get_terminator(), AsmGoto)):
            if len(bloc.predecessors) == 0: # Dead end, delete
                goto : AsmGoto = bloc.get_terminator()
                goto.target.predecessors.remove(bloc)
                self.ir.blocs.remove(bloc)
                if bloc == self.ir.main_bloc:
                    self.ir.main_bloc = goto.target
                
            elif len(bloc.instructions) == 1: # Reduce path
                goto : AsmGoto = bloc.get_terminator()
                if goto.target != bloc:
                    for start in bloc.predecessors:
                        end : Bloc = goto.target
                        # Remove block from end predecessor
                        try:
                            end.predecessors.remove(bloc)
                        except:
                            pass
                        # Add start to end predecessor
                        end.add_predecessor(start)
                        # Replace goto by end in start terminator
                        start.get_terminator().replace(bloc,end)
                    self.ir.blocs.remove(bloc)