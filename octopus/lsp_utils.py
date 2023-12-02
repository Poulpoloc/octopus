from typing import Optional
from octopus.ast_visitor import AstVisitor
from octopus.lex import lexer
from ply.lex import LexToken


def to_lexpos(text : str, position) -> int:
    return sum(map(len,text.replace("\t","    ").split("\n")[:position.line])) + position.line + position.character

def find_token(doc : str, position):
    lexer.lineno = 0
    lexer.input(doc)
    tokens = [t for t in lexer]
    s_pos = to_lexpos(doc, position)
    for i in range(len(tokens)-1):
        if tokens[i].lexpos <= s_pos and tokens[i+1].lexpos > s_pos:
            return tokens[i]
    return None

def get_info(doc : str, position) -> Optional[str]:
    token = find_token(doc, position)
    direct_cost = cost(token)
    if direct_cost:
        return f"*{token.type.lower()} Cost : {direct_cost}*"

def cost(token):
    match token:
        case LexToken(type="ROLL"):
            return "1"
        case LexToken(type="MARK"):
            return "1"
        case LexToken(type="UNMARK"):
            return "1"
        case LexToken(type="PICKUP"):
            return "5"
        case LexToken(type="ATTACK"):
            return "30"
        case LexToken(type="DROP"):
            return "5"
        case LexToken(type="TURN"):
            return "1"
        case LexToken(type="MOVE"):
            return "20"
        case LexToken(type="DIG"):
            return "25"
        case LexToken(type="FILL"):
            return "25"
        case LexToken(type="GRAB"):
            return "20(stunned)+30"    
        case _:
            return None


class InfoVisitor(AstVisitor):
    def search(self, ast,lexpos):
        return ast.accept(self)

    def visit(self, o):
        #print(f"visit {type(o)}")
        if hasattr(o, 'location_span'):
            print(type(o), o.location_span)
        o.accept(self)