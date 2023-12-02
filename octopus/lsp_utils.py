from typing import Optional
from octopus.lex import lexer


def get_info(doc : str, position) -> Optional[str]:
    lexer.input(doc)
    tokens = [t for t in lexer.token()]
    return None