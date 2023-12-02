import ply.yacc as yacc

from octopus.lex import tokens
import octopus.lang_ast as ast

start = 'program'

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'QMARK'),
)

def p_empty(p):
    'empty :'
    pass

def p_declarations_many(p):
    'declarations : declarations declaration'
    p[0] = p[1]
    p[0].append(p[2])
def p_declarations_zero(p):
    'declarations : empty'
    p[0] = []

def p_program(p):
    'program : declarations'
    p[0] = ast.Program(p[1])

def p_base_tantacule_decl(p):
    'declaration : TANTACULE ID LPAR RPAR LBRACE instructions RBRACE'
    p[0] = ast.Tantacule(p[2], p[6], loop=False)
def p_loop_tantacule_decl(p):
    'declaration : LOOP TANTACULE ID LPAR RPAR LBRACE instructions RBRACE'
    p[0] = ast.Tantacule(p[3], p[7], loop=True)

def p_condition_sense(p):
    'condition : smell QMARK sensedir'
    p[0] = ast.Sense(p[1], p[3])

def p_condition_random(p):
    'condition : RAND LPAR NUMBER RPAR'
    p[0] = ast.Rand(p[3])

def p_condition_or(p):
    'condition : condition OR condition'
    p[0] = ast.Or(p[1], p[3])

def p_condition_and(p):
    'condition : condition AND condition'
    p[0] = ast.And(p[1], p[3])

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

def p_instruction_if(p):
    'instruction : IF LPAR condition RPAR LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0] = ast.IfThenElse(condition=p[3], then=p[6], else_=p[10])

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
    'instruction : PICKUP ELSE LBRACE instructions RBRACE'
    p[0] = ast.PickUp(p[4])

def p_instruction_drop(p):
    'instruction : DROP SEMI'
    p[0] = ast.Drop()

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

def p_sense_direction_here(p):
    'sensedir : HERE'
    p[0] = ast.SenseDir.HERE
def p_sense_direction_ahead(p):
    'sensedir : AHEAD'
    p[0] = ast.SenseDir.AHEAD
def p_sense_direction_leftahead(p):
    'sensedir : LEFTAHEAD'
    p[0] = ast.SenseDir.LEFTAHEAD
def p_sense_direction_rightahead(p):
    'sensedir : RIGHTAHEAD'
    p[0] = ast.SenseDir.RIGHTAHEAD
def p_sense_direction_above(p):
    'sensedir : ABOVE'
    p[0] = ast.SenseDir.ABOVE
def p_sense_direction_below(p):
    'sensedir : BELOW'
    p[0] = ast.SenseDir.BELOW

def p_smell_friend(p):
    'smell : FRIEND'
    p[0] = ast.Smell.FRIEND
def p_smell_enemy(p):
    'smell : ENEMY'
    p[0] = ast.Smell.ENEMY
def p_smell_grabbed(p):
    'smell : GRABBED'
    p[0] = ast.Smell.GRABBED
def p_smell_friendwithfood(p):
    'smell : FRIENDWITHFOOD'
    p[0] = ast.Smell.FRIENDWITHFOOD
def p_smell_enemywithfood(p):
    'smell : ENEMYWITHFOOD'
    p[0] = ast.Smell.ENEMYWITHFOOD
def p_smell_food(p):
    'smell : FOOD'
    p[0] = ast.Smell.FOOD
def p_smell_rock(p):
    'smell : ROCK'
    p[0] = ast.Smell.ROCK
def p_smell_empty(p):
    'smell : EMPTY'
    p[0] = ast.Smell.EMPTY
def p_smell_underground(p):
    'smell : UNDERGROUND'
    p[0] = ast.Smell.UNDERGROUND
def p_smell_surface(p):
    'smell : SURFACE'
    p[0] = ast.Smell.SURFACE
def p_smell_holeabove(p):
    'smell : HOLEABOVE'
    p[0] = ast.Smell.HOLEABOVE
def p_smell_holebelow(p):
    'smell : HOLEBELOW'
    p[0] = ast.Smell.HOLEBELOW
def p_smell_marker(p):
    'smell : MARKER'
    p[0] = ast.Smell.MARKER
def p_smell_enemymarker(p):
    'smell : ENEMYMARKER'
    p[0] = ast.Smell.ENEMYMARKER
def p_smell_home(p):
    'smell : HOME'
    p[0] = ast.Smell.HOME
def p_smell_enemyhome(p):
    'smell : ENEMYHOME'
    p[0] = ast.Smell.ENEMYHOME

def p_instruction_turn(p):
    'instruction : TURN direction SEMI'
    p[0] = ast.Turn(p[2])

def p_instruction_move(p):
    'instruction : MOVE movedir SEMI'
    p[0] = ast.Move(None, p[2])
def p_instruction_move_else(p):
    'instruction : MOVE movedir ELSE LBRACE instructions RBRACE'
    p[0] = ast.Move(p[5], p[2])

def p_instruction_dig(p):
    'instruction : DIG movedir SEMI'
    p[0] = ast.Dig(None, p[2])
def p_instruction_dig_else(p):
    'instruction : DIG movedir ELSE LBRACE instructions RBRACE'
    p[0] = ast.Dig(p[5], p[2])

def p_instruction_fill(p):
    'instruction : FILL movedir SEMI'
    p[0] = ast.Fill(None, p[2])
def p_instruction_fill_else(p):
    'instruction : FILL movedir ELSE LBRACE instructions RBRACE'
    p[0] = ast.Fill(p[5], p[2])

def p_instruction_grab(p):
    'instruction : GRAB SEMI'
    p[0] = ast.Grab(None)
def p_instruction_grab_else(p):
    'instruction : GRAB ELSE LBRACE instructions RBRACE'
    p[0] = ast.Grab(p[4])

def p_instruction_attack(p):
    'instruction : ATTACK SEMI'
    p[0] = ast.Attack(None)
def p_instruction_attack_else(p):
    'instruction : ATTACK ELSE LBRACE instructions RBRACE'
    p[0] = ast.Attack(p[4])


def p_error(t):
    print(f"Syntax error, unexpected token {t.type}")

parser = yacc.yacc()
