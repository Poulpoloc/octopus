from octopus.yacc import parser
import argparse
import os
from ast_visitor import AstVisitor

def main():
    arg_parser = argparse.ArgumentParser(description='Compile ant')
    arg_parser.add_argument('input', type=str, 
                    help='File to compile')
    args = arg_parser.parse_args()
    with open(os.path.abspath(args.input), 'r') as f:
        input_string = f.read()
        expression = parser.parse(input_string)
        visitor = AstVisitor()
        visitor.visit(expression)
        print(expression)

if "__main__" in __name__:
    main()
