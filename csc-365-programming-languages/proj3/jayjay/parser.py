'''
Created on Jan 2, 2014

@author: tvandrun
'''
import sys
sys.path.append(".")
sys.path.append("..")
from ply.lex import lex
from ply.yacc import yacc
from jay.ast_values import *
from jayjay_ast import *

def buildBin(x, (op, y)) :
    return BinaryExpr(x, op, y)

# lexer

reserved = {
    'public' : 'PUB',
    'class' : 'CLS',
    'static' : 'STC',
    'void' : 'VD',
    'main' : 'MN',
    'String' : 'STR',
    'args' : 'ARGS',
    'int' : 'INT',
    'boolean' : 'BOOL',
    'if' : 'IF',
    'else' : 'ELSE', 
    'while' : 'WHILE',
    'System' : 'SYS',
    'out' : 'OUT',
    'println' : 'PRNTLN',
    'for' : 'FOR',
    'do' : 'DO' } 


tokens = ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRCKT', 'RBRCKT', 'SEMI', 'COMMA', 'DOT',
          'ASGN',
          'AND', 'OR', 'PLUS', 'MINUS', 'STAR', 'SLASH', 'BANG',
          'LT', 'LTEQ', 'GT', 'GTEQ', 'EQ', 'NEQ',
           #'PRINT',
          'INTEGER', 'BOOLEAN', 'ID', 'CAPID'] + list(reserved.values())


t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRCKT = r'\['
t_RBRCKT = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COMMA = r','
t_DOT = r'\.'

t_ASGN = r'=';

t_AND = r'&&';
t_OR = r'\|\|';
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_STAR   = r'\*'
t_SLASH  = r'/'
t_BANG = r'!';
t_LT = r'<';
t_LTEQ = r'<=';
t_GT = r'>';
t_GTEQ = r'>=';
t_EQ = r'==';
t_NEQ = r'!=';


def t_INTEGER(t):
    r'0|([1-9]\d*)'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'(true|false)'
    t.value = t.value == "true"
    return t

def t_ID(t):
    r'[a-z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_CAPID(t):
    r'[A-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'CAPID')    # Check for reserved words
    return t

t_ignore = " \t\n"

simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
string_char = r"""([^"\\\n]|"""+simple_escape+')'   
string_literal = '"'+string_char+'*"'

t_ignore_LINE_COMMENT = r'//.*'

# I haven't yet figured out how to do block comments yet

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# parser

def p_program(p) :
    ' program : PUB CLS CAPID LBRACE PUB STC VD MN LPAREN STR LBRCKT RBRCKT ARGS RPAREN LBRACE declarations statements RBRACE RBRACE '
    p[0] = Program(Block(p[16], p[17]))

def p_declarations(p) :
    """declarations : declaration declarations 
             | """
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [p[1]] + p[2]

def p_declaration(p) :
    ' declaration : type identifiers SEMI '
    p[0] = Declaration(p[1], p[2])

def p_type(p) :
    """ type : INT 
        | BOOL """
    p[0] = p[1]   # I hate that

def p_identifiers(p) :
    ' identifiers : ID moreIdentifiers '
    p[0] = [p[1]] + p[2]

def p_moreIdentifiers(p) :
    """moreIdentifiers : COMMA ID moreIdentifiers 
        | """
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [p[2]] + p[3]
        
def p_statements(p) :
    """statements : statement statements 
        | """
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [p[1]] + p[2]

def p_statement(p):
    """statement : skip 
        | block 
        | assignment 
        | ifStatement 
        | whileStatement 
        | printStatement
        | forStatement
        | doWhileStatement """
    
    p[0] = p[1]
    
def p_skip(p):
    'skip : SEMI '
    p[0] = Skip()
    
def p_block(p):
    'block : LBRACE declarations statements RBRACE '
    p[0] = Block(p[2], p[3])

def p_assignment(p):
    'assignment : ID ASGN expression SEMI '
    p[0] = Assignment(p[1], p[3])

def p_ifStatement(p):
    'ifStatement : IF LPAREN expression RPAREN statement elseOptional'
    p[0] = Conditional(p[3], p[5], p[6])

def p_elseOptional(p):
    """elseOptional : ELSE statement
        | """
    if len(p) == 1 :
        p[0] = Skip()
    else :
        p[0] = p[2]
        
    
def p_whileStatement(p):
    'whileStatement : WHILE LPAREN expression RPAREN statement'
    p[0] = Loop(p[3], p[5])

def p_printStatement(p):
    'printStatement : SYS DOT OUT DOT PRNTLN LPAREN expression RPAREN SEMI'
    p[0] = Print(p[7])

def p_forStatement(p):
    'forStatement : FOR LPAREN initializer SEMI expressionOptional SEMI increment RPAREN statement'
    p[0] = CountLoop(p[3], p[5], p[7], p[9])

def p_initializer(p):
    """initializer : typeOptional ID ASGN expression
    | """
    if p[1] == None :
        p[0] = NonDeclInitializer(p[2], p[4])
    else :
        p[0] = DeclInitializer(p[1], p[2], p[4])
    # why bother having separate classes for NonDeclInitializer and DeclInitializer,
    # why not just leave the first attribute None? Because the code is pretty
    # different for these two AST kinds in the visitors

def p_typeOptional(p) :
    """ typeOptional : type
        | """
    if len(p) == 1 :
        p[0] = None
    else :
        p[0] = p[1]

# dumb parser generator that can't handle regex notation
def p_expressionOptional(p):
    """expressionOptional : expression
        | """
    if len(p) == 1 :
        p[0] = None
    else :
        p[0] = p[1]

def p_increment(p):
    """increment : ID ASGN expression
        | """
    if len(p) == 1 :
        p[0] = None
    else :
        p[0] = Assignment(p[1], p[3]) 

def p_doWhileStatement(p): 
    'doWhileStatement : DO statement WHILE LPAREN expression RPAREN SEMI'
    p[0] = PTLoop(p[2], p[5])
    
def p_expression(p):
    'expression : conjunction moreConjunctions'
    p[0] = reduce(buildBin, p[2], p[1])

def p_moreConjunctions(p):
    """moreConjunctions : OR conjunction moreConjunctions 
        | """
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [(binOps[p[1]], p[2])] + p[3]

def p_conjunction(p):
    'conjunction : relation moreRelations'
    p[0] = reduce(buildBin, p[2], p[1])

def p_moreRelations(p):
    """moreRelations : AND relation moreRelations 
        | """
    
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [(binOps[p[1]], p[2])] + p[3]

def p_relation(p):
    """relation : addition relOp addition 
        | addition """
    if len(p) == 2 :
        p[0] =  p[1]
    else :
        p[0] = BinaryExpr(p[1], binOps[p[2]], p[3])

def p_relOp(p):
    """relOp : LT 
        | LTEQ 
        | GT 
        | GTEQ 
        | EQ 
        | NEQ """
    p[0] = p[1]

def p_addition(p):
    'addition : term moreTerms  '
    p[0] = reduce(buildBin, p[2], p[1])

def p_moreTerms(p):
    """moreTerms : addOp term moreTerms 
        | """
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [(p[1], p[2])] + p[3] 

def p_addOp(p):
    """ addOp : PLUS 
        | MINUS """
    p[0] = binOps[p[1]]

def p_term(p) :
    'term : negation moreNegations'  
    p[0] = reduce(buildBin, p[2], p[1])
    
def p_moreNegations(p):
    """ moreNegations : mulOp negation moreNegations
            | """
    if len(p) == 1 :
        p[0] = []
    else :
        p[0] = [(p[1], p[2])] + p[3] 
    
def p_mulOp(p):
    """ mulOp : STAR 
        | SLASH """
    p[0] = binOps[p[1]]
    
def p_negation(p):
    """negation : negOp factor 
        | factor """
    p[0] = UnaryExpr(p[1], p[2]) if len(p) == 3 else p[1]

def p_negOp(p):
    """negOp : BANG 
        | MINUS"""
    p[0] = p[1]
    
def p_factor(p):
    """factor : variable 
        | intLiteral 
        | boolLiteral 
        | parenthesized """
    p[0] = p[1] 
    
def p_variable(p):
    'variable : ID'
    p[0] = Variable(p[1])

def p_intLiteral(p): 
    'intLiteral : INTEGER'
    p[0] = IntLitExpr(p[1])
    
def p_boolLiteral(p):
    'boolLiteral : BOOLEAN'  
    p[0] = BoolLitExpr(p[1])
    
def p_parenthesized(p):
    'parenthesized : LPAREN expression RPAREN'
    p[0] = p[2]
    
# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

lexer = lex(lextab="jayjay_lextab.py")
parser = yacc(tabmodule="jayjay_parsetab.py", debug=False)
