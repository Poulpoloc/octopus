from octopus.yacc import parser, parser_report
from octopus.codegen import CodeGenVisitor
from octopus.ir_builder  import IRBuilderVisitor
from octopus.ir_codegen  import IRCodeGenerator
from octopus.compiler_report import CompilerReport
import argparse
import os

def get_report(path):
    with open(os.path.abspath(path), 'r') as f:
        input_string = f.read()
        # Martin qui fait de la magie noire ...
        # Ici martin décide de mélanger les objet avec la classe 
        # Mais bon, ça marche, et on est en Python, on lui en veut pas
        CompilerReport.reset(CompilerReport) # type: ignore
        expression = parser.parse(input_string, tracking=True)
        return parser_report

def main():
    arg_parser = argparse.ArgumentParser(description='Compile ant')
    arg_parser.add_argument('input', type=str, 
                    help='File to compile')
    arg_parser.add_argument('--output', "-o", type=str, 
                    help='File to store')
    args = arg_parser.parse_args()
    with open(os.path.abspath(args.input), 'r') as f:
        input_string = f.read()
        expression = parser.parse(input_string, tracking=True)
        print(parser_report)

        visitor = CodeGenVisitor()
        visitor.visit(expression)

        irbuilder = IRBuilderVisitor()
        irbuilder.visit(expression)

        codegen = IRCodeGenerator()
        codegen.visit(irbuilder.ir)

        #assembly_code = visitor.get_code()
        assembly_code = codegen.code.to_string()
        if args.output:
            with open(args.output,'w') as fo:
                fo.write(assembly_code)
        else:
            print("Produced code:")
            print(assembly_code)

if "__main__" in __name__:
    main()
