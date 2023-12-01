import ply.yacc as yacc

from octopus.lex import tokens
import octopus.lang_ast as ast

start = 'expression'

precedence = (
    ('nonassoc', 'IN'),
    ('left', 'PLUS')
)

def p_expression_plus(p):
    'expression : expression PLUS expression'
    p[0] = ast.Plus(p[1], p[3])

def p_expression_atom(p):
    '''expression : NUMBER
                  | ID'''
    if type(p[1]) == int:
        p[0] = ast.Int(p[1])
    else:
        p[0] = ast.Var(p[1])

def p_expression_embraced(p):
    'expression : LPAR expression RPAR'
    p[0] = p[2]

def p_expression_letin(p):
    'expression : LET ID EQUAL expression IN expression'
    p[0] = ast.LetIn(p[2], p[4], p[6])


def p_error(t):
    print(f"Syntax error, unexpected token {t.type}")

parser = yacc.yacc()
