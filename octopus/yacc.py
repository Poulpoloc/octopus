import ply.yacc as yacc

from octopus.lex import tokens
import octopus.lang_ast as ast

from octopus.compiler_report import CompilerReport, CRWarning, CRError
parser_report = CompilerReport()

start = 'program'

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'BANG'),
    ('nonassoc', 'QMARK'),
)

def save_location(p):
    p[0].location_span = p.lexpos(1), p.lexspan(-1)[1]

def p_empty(p):
    'empty :'
    pass

def p_integer(p):
    'integer : NUMBER'
    p[0] = ast.Number(p[1])
def p_intvar(p):
    'integer : ID'
    p[0] = ast.IntVar(p[1])

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
    save_location(p)
def p_loop_tantacule_decl(p):
    'declaration : LOOP TANTACULE ID LPAR RPAR LBRACE instructions RBRACE'
    p[0] = ast.Tantacule(p[3], p[7], loop=True)
    save_location(p)
def p_macro_decl(p):
    'declaration : DEF ID LPAR RPAR LBRACE instructions RBRACE'
    p[0] = ast.Macro(p[2], p[6])
    save_location(p)
def p_bool_decl(p):
    'declaration : BOOL ID EQ condition SEMI'
    p[0] = ast.ConstBool(p[2], p[4])
    save_location(p)
def p_int_decl(p):
    'declaration : INT ID EQ NUMBER SEMI'
    p[0] = ast.ConstInt(p[2], p[4])
    save_location(p)

def p_condition_par(p):
    'condition : LPAR condition RPAR'
    p[0] = p[2]
    save_location(p)

def p_condition_var(p):
    'condition : ID'
    p[0] = ast.CondVar(p[1])
    save_location(p)

def p_condition_sense(p):
    'condition : smell QMARK sensedir'
    p[0] = ast.Sense(p[1], p[3])
    save_location(p)

def p_condition_random(p):
    'condition : RAND LPAR integer RPAR'
    p[0] = ast.Rand(p[3])
    save_location(p)

def p_condition_not(p):
    'condition : BANG condition'
    p[0] = ast.Not(p[2])
    save_location(p)

def p_condition_or(p):
    'condition : condition OR condition'
    p[0] = ast.Or(p[1], p[3])
    save_location(p)

def p_condition_and(p):
    'condition : condition AND condition'
    p[0] = ast.And(p[1], p[3])
    save_location(p)

def p_instructions_many(p):
    'instructions : instructions instruction'
    p[0] = p[1]
    p[0].append(p[2])
def p_instructions_zero(p):
    'instructions : empty'
    p[0] = []

def p_instruction_repeat(p):
    'instruction : REPEAT integer LBRACE instructions RBRACE'
    p[0] = ast.Repeat(p[2], p[4])
    save_location(p)

def p_instruction_if(p):
    'instruction : IF LPAR condition RPAR LBRACE instructions RBRACE'
    p[0] = ast.IfThenElse(condition=p[3], then=p[6], else_=[])
    save_location(p)
def p_instruction_ifelse(p):
    'instruction : IF LPAR condition RPAR LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0] = ast.IfThenElse(condition=p[3], then=p[6], else_=p[10])
    save_location(p)

def p_instruction_while(p):
    'instruction : WHILE LPAR condition RPAR LBRACE instructions RBRACE'
    p[0] = ast.While(condition=p[3], instructions=p[6])
    save_location(p)

def p_cases_many(p):
    'cases : cases case'
    p[0] = p[1]
    p[0].append(p[2])
def p_cases_zero(p):
    'cases : empty'
    p[0] = []

def p_case(p):
    'case : ARROW LBRACE instructions RBRACE'
    p[0] = p[3]

def p_instruction_roll(p):
    'instruction : ROLL integer cases'
    p[0] = ast.Roll(p[2], p[3])
    save_location(p)

def p_instructin_call(p):
    'instruction : ID LPAR RPAR SEMI'
    p[0] = ast.Call(p[1])
    save_location(p)

def p_instruction_slideto(p):
    'instruction : SLIDETO ID SEMI'
    p[0] = ast.SlideTo(p[2])
    save_location(p)
def p_instruction_slideback(p):
    'instruction : SLIDEBACK SEMI'
    p[0] = ast.SlideBack()
    save_location(p)

def p_instruction_mark(p):
    'instruction : MARK LPAR integer RPAR SEMI'
    p[0] = ast.Mark(p[3])
    save_location(p)
def p_instruction_unmark(p):
    'instruction : UNMARK LPAR integer RPAR SEMI'
    if p[3] >= 8:
        warning = CRWarning("Marker is too large.", p.lexspan(3))
        parser_report.warning(warning)
    p[0] = ast.Unmark(p[3])
    save_location(p)

def p_instruction_pickup(p):
    'instruction : PICKUP SEMI'
    p[0] = ast.PickUp(None)
    save_location(p)
def p_instruction_pickup_else(p):
    'instruction : PICKUP ELSE LBRACE instructions RBRACE'
    if len(p[4]) == 0:
        warning = CRWarning("Empty handler.", (p.lexpos(3), p.lexpos(5)))
        parser_report.warning(warning)
    p[0] = ast.PickUp(p[4])
    save_location(p)

def p_instruction_drop(p):
    'instruction : DROP SEMI'
    p[0] = ast.Drop()
    save_location(p)

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
    p[0] = ast.AtomicSmell.FRIEND
def p_smell_enemy(p):
    'smell : ENEMY'
    p[0] = ast.AtomicSmell.ENEMY
def p_smell_grabbed(p):
    'smell : GRABBED'
    p[0] = ast.AtomicSmell.GRABBED
def p_smell_friendwithfood(p):
    'smell : FRIENDWITHFOOD'
    p[0] = ast.AtomicSmell.FRIENDWITHFOOD
def p_smell_enemywithfood(p):
    'smell : ENEMYWITHFOOD'
    p[0] = ast.AtomicSmell.ENEMYWITHFOOD
def p_smell_food(p):
    'smell : FOOD'
    p[0] = ast.AtomicSmell.FOOD
def p_smell_rock(p):
    'smell : ROCK'
    p[0] = ast.AtomicSmell.ROCK
def p_smell_empty(p):
    'smell : EMPTY'
    p[0] = ast.AtomicSmell.EMPTY
def p_smell_underground(p):
    'smell : UNDERGROUND'
    p[0] = ast.AtomicSmell.UNDERGROUND
def p_smell_surface(p):
    'smell : SURFACE'
    p[0] = ast.AtomicSmell.SURFACE
def p_smell_holeabove(p):
    'smell : HOLEABOVE'
    p[0] = ast.AtomicSmell.HOLEABOVE
def p_smell_holebelow(p):
    'smell : HOLEBELOW'
    p[0] = ast.AtomicSmell.HOLEBELOW
def p_smell_marker(p):
    'smell : MARKER LPAR integer RPAR'
    p[0] = ast.Marker(p[3])
def p_smell_enemymarker(p):
    'smell : ENEMYMARKER'
    p[0] = ast.AtomicSmell.ENEMYMARKER
def p_smell_home(p):
    'smell : HOME'
    p[0] = ast.AtomicSmell.HOME
def p_smell_enemyhome(p):
    'smell : ENEMYHOME'
    p[0] = ast.AtomicSmell.ENEMYHOME

def p_instruction_turn(p):
    'instruction : TURN direction SEMI'
    p[0] = ast.Turn(p[2])

def p_instruction_move(p):
    'instruction : MOVE movedir SEMI'
    p[0] = ast.Move(None, p[2])
    save_location(p)
def p_instruction_move_else(p):
    'instruction : MOVE movedir ELSE LBRACE instructions RBRACE'
    if len(p[5]) == 0:
        warning = CRWarning("Empty handler.", (p.lexpos(4), p.lexpos(6)))
        parser_report.warning(warning)
    p[0] = ast.Move(p[5], p[2])
    save_location(p)

def p_instruction_dig(p):
    'instruction : DIG movedir SEMI'
    p[0] = ast.Dig(None, p[2])
    save_location(p)
def p_instruction_dig_else(p):
    'instruction : DIG movedir ELSE LBRACE instructions RBRACE'
    if len(p[5]) == 0:
        warning = CRWarning("Empty handler.", (p.lexpos(4), p.lexpos(6)))
        parser_report.warning(warning)
    p[0] = ast.Dig(p[5], p[2])
    save_location(p)

def p_instruction_fill(p):
    'instruction : FILL movedir SEMI'
    p[0] = ast.Fill(None, p[2])
    save_location(p)
def p_instruction_fill_else(p):
    'instruction : FILL movedir ELSE LBRACE instructions RBRACE'
    if len(p[5]) == 0:
        warning = CRWarning("Empty handler.", (p.lexpos(4), p.lexpos(6)))
        parser_report.warning(warning)
    p[0] = ast.Fill(p[5], p[2])
    save_location(p)

def p_instruction_grab(p):
    'instruction : GRAB SEMI'
    p[0] = ast.Grab(None)
    save_location(p)
def p_instruction_grab_else(p):
    'instruction : GRAB ELSE LBRACE instructions RBRACE'
    if len(p[4]) == 0:
        warning = CRWarning("Empty handler.", (p.lexpos(3), p.lexpos(5)))
        parser_report.warning(warning)
    p[0] = ast.Grab(p[4])
    save_location(p)

def p_instruction_attack(p):
    'instruction : ATTACK SEMI'
    p[0] = ast.Attack(None)
    save_location(p)
def p_instruction_attack_else(p):
    'instruction : ATTACK ELSE LBRACE instructions RBRACE'
    if len(p[4]) == 0:
        warning = CRWarning("Empty handler.", (p.lexpos(3), p.lexpos(5)))
        parser_report.warning(warning)
    p[0] = ast.Attack(p[4])
    save_location(p)


def p_error(t):
    if t is not None:
        error = CRError("Syntax Error.", (t.lexpos, t.lexpos))
        parser_report.error(error)
        print(f"Syntax error, unexpected token {t.type}")
    else:
        print(f"Syntax error, unexpected token {t.type}")

parser = yacc.yacc()
