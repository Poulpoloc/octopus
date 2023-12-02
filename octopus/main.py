from octopus.yacc import parser
from octopus.codegen import CodeGenVisitor
import argparse
import os

def main():
    arg_parser = argparse.ArgumentParser(description='Compile ant')
    arg_parser.add_argument('input', type=str, 
                    help='File to compile')
    arg_parser.add_argument('--output', "-o", type=str, 
                    help='File to store')
    args = arg_parser.parse_args()
    with open(os.path.abspath(args.input), 'r') as f:
        input_string = f.read()
        expression = parser.parse(input_string)

        visitor = CodeGenVisitor()
        visitor.visit(expression)

        #print(expression)

        assembly_code = visitor.get_code()
        if args.output:
            with open(args.output,'w') as fo:
                fo.write(assembly_code)
        else:
            print("Produced code:")
            print(assembly_code)

if "__main__" in __name__:
    main()
