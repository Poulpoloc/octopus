from octopus.ir_visitor import IRVisitor
from octopus.ir import *

class IRDeadCodeOptimizer(IRVisitor):
    def visit_ir(self, ir: IR):
        self.ir = ir
        self.accessible = {}
        self.visit(self.ir.main_bloc)
        ir.blocs = [b for b in self.ir.blocs if b in self.accessible]

    
    def visit_bloc(self, bloc: Bloc):
        self.accessible[bloc] = True
        term = bloc.get_terminator()
        for succ in term.get_successors():
            if not succ in self.accessible:
                self.visit(succ)
        


class IRGotoOptimizer(IRVisitor):

    def visit_ir(self, ir: IR):
        self.ir = ir
        ir.blocs = [b for b in ir.blocs if len(b.instructions)>0]
        before,after = len(ir.blocs), len(ir.blocs)-1
        while before!=after: # Point fixe
            print("IR Loop")
            assert ir.main_bloc in ir.blocs
            before = len(ir.blocs)
            self.to_delete = []
            for bloc in sorted(ir.blocs, key=lambda b: len(b.predecessors)):
                self.visit(bloc)
            ir.blocs = [b for b in self.ir.blocs if not b in self.to_delete]
            after = len(ir.blocs)
        # Inline dead optio
        assert ir.main_bloc in ir.blocs
        opti = IRDeadCodeOptimizer()
        ir.accept(opti)
        assert ir.main_bloc in ir.blocs



    def visit_bloc(self, bloc: Bloc):
        if(isinstance(bloc.get_terminator(), AsmGoto)):
            if len(bloc.predecessors) == 0: # Dead end, delete
                goto : AsmGoto = bloc.get_terminator()
                try:
                    goto.target.predecessors.remove(bloc)
                except:
                    pass
                self.to_delete.append(bloc)
                if bloc == self.ir.main_bloc:
                    assert goto.target not in self.to_delete
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
                        if bloc == self.ir.main_bloc:
                            assert start not in self.to_delete
                            self.ir.main_bloc = start
                    self.to_delete.append(bloc)
        """
        elif len(bloc.instructions) == 1 and len(bloc.predecessors) == 0 and bloc != self.ir.main_bloc: # Dead Code elimination
            termin = bloc.get_terminator()
            if hasattr(termin, "target"):
                try: termin.target.predecessors.remove(bloc)
                except: pass
                self.to_delete.append(bloc)
                if bloc == self.ir.main_bloc:
                    self.ir.main_bloc = termin.target
            elif hasattr(termin, "then"):
                try: termin.then.predecessors.remove(bloc)
                except: pass
                try: termin.else_.predecessors.remove(bloc)
                except: pass
                self.to_delete.append(bloc)
                if bloc == self.ir.main_bloc:
                    self.ir.main_bloc = termin.then
            elif hasattr(termin, "follower"):
                try: termin.follower.predecessors.remove(bloc)
                except: pass
                try: termin.handler.predecessors.remove(bloc)
                except: pass
                self.to_delete.append(bloc)
                if bloc == self.ir.main_bloc:
                    self.ir.main_bloc = termin.follower"""
            

        