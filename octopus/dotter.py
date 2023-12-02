from octopus.iroptim import IRGotoOptimizer
from octopus.irtodot import IRDotGenerator
from octopus.yacc import parser, parser_report
from octopus.codegen import CodeGenVisitor
from octopus.ir_builder  import IRBuilderVisitor
from octopus.ir_codegen  import IRCodeGenerator
from octopus.compiler_report import CompilerReport
import argparse
import os

def dotter():
    arg_parser = argparse.ArgumentParser(description='Draw CFG ant')
    arg_parser.add_argument('input', type=str, 
                    help='File to draw')
    arg_parser.add_argument('--output', "-o", type=str, 
                    help='File to store')
    args = arg_parser.parse_args()
    with open(os.path.abspath(args.input), 'r') as f:
        input_string = f.read()
        expression = parser.parse(input_string, tracking=True)
        print(parser_report)

        irbuilder = IRBuilderVisitor()
        irbuilder.visit(expression)

        optimizer = IRGotoOptimizer()
        irbuilder.ir.accept(optimizer)

        ir = irbuilder.ir

        gen = IRDotGenerator()
        text = gen.generate(ir)

        if args.output:
            with open(f"{args.output}.dot",'w') as fo:
                fo.write(text)
            os.system(f"dot -T png -o {args.output} {args.output}.dot")
            os.system(f"rm {args.output}.dot")
        else:
            print(text)

if "__main__" in __name__:
    dotter()