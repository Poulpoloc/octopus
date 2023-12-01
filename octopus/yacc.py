import ply.yacc as yacc

from octopus.lex import tokens
import octopus.lang_ast as ast

start = 'declaration'

precedence = (
    #('left', 'PLUS')
)

def p_empty(p):
    'empty :'
    pass

def p_base_tantacule_decl(p):
    'declaration : TANTACULE ID LPAR RPAR LBRACE instructions RBRACE'
    p[0] = ast.Tantacule(p[2], p[6], loop=False)
def p_loop_tantacule_decl(p):
    'declaration : LOOP TANTACULE ID LPAR RPAR LBRACE instructions RBRACE'
    p[0] = ast.Tantacule(p[3], p[7], loop=True)


def p_instructions_many(p):
    'instructions : instructions instruction'
    p[0] = p[1]
    p[0].append(p[2])

def p_instructions_zero(p):
    'instructions : empty'
    p[0] = []

def p_instruction_repeat(p):
    'instruction : REPEAT NUMBER LBRACE instructions RBRACE'
    p[0] = ast.Repeat(p[2], p[4])

def p_instruction_slideto(p):
    'instruction : SLIDETO ID SEMI'
    p[0] = ast.SlideTo(p[2])
def p_instruction_slideback(p):
    'instruction : SLIDEBACK SEMI'
    p[0] = ast.SlideBack()

def p_instruction_mark(p):
    'instruction : MARK LPAR NUMBER RPAR SEMI'
    p[0] = ast.Mark(p[3])
def p_instruction_unmark(p):
    'instruction : UNMARK LPAR NUMBER RPAR SEMI'
    p[0] = ast.Unmark(p[3])

def p_instruction_pickup(p):
    'instruction : PICKUP SEMI'
    p[0] = ast.PickUp(None)
def p_instruction_pickup_else(p):
    'instruction : PICKUP ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.PickUp(p[4])

def p_instruction_drop(p):
    'instruction : DROP SEMI'
    p[0] = ast.Drop(None)
def p_instruction_drop_else(p):
    'instruction : DROP ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.Drop(p[4])

def p_direction_left(p):
    'direction : LEFT'
    p[0] = ast.Direction.LEFT
def p_direction_right(p):
    'direction : RIGHT'
    p[0] = ast.Direction.RIGHT

def p_move_direction_up(p):
    'movedir : UP'
    p[0] = ast.MoveDir.UP
def p_move_direction_down(p):
    'movedir : DOWN'
    p[0] = ast.MoveDir.DOWN
def p_move_direction_empty(p):
    'movedir : empty'
    p[0] = ast.MoveDir.FORWARD

def p_instruction_turn(p):
    'instruction : TURN direction SEMI'
    p[0] = ast.Turn(p[2])

def p_instruction_move(p):
    'instruction : MOVE movedir SEMI'
    p[0] = ast.Move(None, p[2])
def p_instruction_move_else(p):
    'instruction : MOVE movedir ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.Move(p[5], p[2])

def p_instruction_dig(p):
    'instruction : DIG movedir SEMI'
    p[0] = ast.Dig(None, p[2])
def p_instruction_dig_else(p):
    'instruction : DIG movedir ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.Dig(p[5], p[2])

def p_instruction_fill(p):
    'instruction : FILL movedir SEMI'
    p[0] = ast.Fill(None, p[2])
def p_instruction_fill_else(p):
    'instruction : FILL movedir ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.Fill(p[5], p[2])

def p_instruction_grab(p):
    'instruction : GRAB SEMI'
    p[0] = ast.Grab(None)
def p_instruction_grab_else(p):
    'instruction : GRAB ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.Grab(p[4])

def p_instruction_attack(p):
    'instruction : ATTACK SEMI'
    p[0] = ast.Attack(None)
def p_instruction_attack_else(p):
    'instruction : ATTACK ELSE LBRACE instructions RBRACE SEMI'
    p[0] = ast.Attack(p[4])


def p_error(t):
    print(f"Syntax error, unexpected token {t.type}")

parser = yacc.yacc()
