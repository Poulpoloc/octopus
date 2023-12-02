from typing import Optional
from octopus.lex import lexer
from ply.lex import LexToken


def to_lexpos(text : str, position) -> int:
    return sum(map(len,text.split("\n")[:position.line])) + position.character

def find_token(doc : str, position):
    lexer.input(doc)
    tokens = [t for t in lexer]
    s_pos = to_lexpos(doc, position)
    for i in range(len(tokens)-1):
        if tokens[i].lexpos <= s_pos and tokens[i].lexpos > s_pos:
            return tokens[i]
    return None

def get_info(doc : str, position) -> Optional[str]:
    token = find_token(doc, position)
    if token:
        match token:
            case LexToken(type="TANTACULE"):
                return "***ATTENTION***"
    return None