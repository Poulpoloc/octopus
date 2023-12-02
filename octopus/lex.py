import ply.lex as lex
from ply.lex import TOKEN

keywords = {
    "tantacule": 'TANTACULE',
    "def": 'DEF',
    "looping": 'LOOP',
    "slideto": 'SLIDETO',
    "slideback": 'SLIDEBACK',
    "repeat": 'REPEAT',
    "if": 'IF',
    "else": 'ELSE',
    "while": 'WHILE',
    "roll": 'ROLL',

    "mark": 'MARK',
    "unmark": 'UNMARK',
    "pickup": 'PICKUP',
    "attack": 'ATTACK',
    "drop": 'DROP',
    "turn": 'TURN',
    "move": 'MOVE',
    "dig": 'DIG',
    "fill": 'FILL',
    "grab": 'GRAB',

    "left": 'LEFT',
    "up": 'UP',
    "down": 'DOWN',
    "right": 'RIGHT',

    "rand": 'RAND',
    "here": 'HERE',
    "ahead": 'AHEAD',
    "leftahead": 'LEFTAHEAD',
    "rightahead": 'RIGHTAHEAD',
    "above": 'ABOVE',
    "below": 'BELOW',

    "friend": 'FRIEND',
    "enemy": 'ENEMY',
    "grabbed": 'GRABBED',
    "friendwithfood": 'FRIENDWITHFOOD',
    "enemywithfood": 'ENEMYWITHFOOD',
    "food": 'FOOD',
    "rock": 'ROCK',
    "empty": 'EMPTY',
    "underground": 'UNDERGROUND',
    "surface": 'SURFACE',
    "holeabove": 'HOLEABOVE',
    "holebelow": 'HOLEBELOW',
    "marker": 'MARKER',
    "enemymarker": 'ENEMYMARKER',
    "home": 'HOME',
    "enemyhome": 'ENEMYHOME',
}

tokens = [
    'ID',
    'NUMBER',
    'LPAR',
    'RPAR',
    'LBRACE',
    'RBRACE',
    'SEMI',
    'QMARK',
    'BANG',
    'OR',
    'AND',
    'ARROW',
] + list(keywords.values())

states = [('comment', 'exclusive')]

@TOKEN(r'\d+')
def t_NUMBER(t):
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
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_QMARK = r'\?'
t_BANG = r'\!'
t_OR = r'\|\|'
t_AND = r'&&'
t_ARROW = r'\|\-\>'


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
