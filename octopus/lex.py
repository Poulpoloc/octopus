import ply.lex as lex
from ply.lex import TOKEN

keywords = {
    'let' : 'LET',
    'in'  : 'IN'
}

tokens = [
    'NUMBER',
    'ID',
    'PLUS',
    'EQUAL',
    'LPAR',
    'RPAR'
] + list(keywords.values())

states = [('comment', 'exclusive')]

# Lex a number and convert to an integer
@TOKEN(r'\d+')
def t_NUMBER(t):
    # You can specify the regex with the TOKEN decorator
    # _or_ in the function's docstring
    t.value = int(t.value)
    return t

@TOKEN(r'[a-zA-Z][a-zA-Z0-9_]*')
def t_ID(t):
    # If t is a keyword, change its type
    t.type = keywords.get(t.value, t.type)
    return t

# Skip one or more newlines
@TOKEN(r'\n+')
def t_newline(t):
    t.lexer.lineno += len(t.value)

# Simple tokens can be defined as strings
t_PLUS = r'\+'
t_EQUAL = r'\='
t_LPAR = r'\('
t_RPAR = r'\)'


# Comments handling
@TOKEN(r'//.*')
def t_COMMENT(t):
    # No return value, token is discarded
    pass

@TOKEN(r'/\*')
def t_ANY_opencmt(t):
    t.lexer.push_state('comment')

@TOKEN(r'.*\*/')
def t_comment_closecmt(t):
    t.lexer.pop_state()


# Special and reserved rule
t_ANY_ignore = ' \t'

def t_ANY_error(t):
    # t.value contains the rest of the input
    print(f"Illegal character '{t.value[0]}'.")
    t.lexer.skip(1)


lexer = lex.lex()

"""
lexer.input("let x = 1 + /* téma le /* imbriqué */ commentaire */ 2 in // comment \n x + y")

while True:
    tok = lexer.token()
    if tok is None:
        break;
    print(tok.type, tok.value)
"""
