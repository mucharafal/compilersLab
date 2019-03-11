#!/usr/bin/python
import ply.lex as lex
import sys
import ply.yacc as yacc

tokens = (  'PLUS',  'MINUS',  'MUL',  'DIVIDE',
	'DOTPLUS', 'DOTMINUS', 'DOTMUL', 'DOTDIVIDE', 'ASS', 'ASSPLUS', 'ASSMINUS', 'ASSMUL', 		'ASSDIVIDE', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ', 'LPAR', 'RPAR', 'LSQBR', 'RSQBR', 'LBR',
	'RBR', 'RNG', 'TRANS', 'COMMA', 'SCOL', 'IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE',
	'RETURN', 'EYE', 'ZEROS', 'ONES', 'PRINT', 'ID', 'INT', 'FLOAT', 'STRING')

t_DOTPLUS = r'\.\+'
t_DOTMINUS = r'\.\-'
t_DOTMUL = r'\.\*'
t_DOTDIVIDE = r'\./'
t_ASSPLUS = r'\+='
t_ASSMINUS = r'\-='
t_ASSMUL = r'\*='
t_ASSDIVIDE = r'/='
t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_EQ = r'=='
t_LT = r'<'
t_GT = r'>'
t_ASS = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MUL   = r'\*'
t_DIVIDE  = r'/'
t_LPAR  = r'\('
t_RPAR  = r'\)'
t_LSQBR = r'\['
t_RSQBR = r'\]'
t_LBR = r'\{'
t_RBR = r'\}'
t_RNG = r'\:'
t_TRANS = r'\''
t_COMMA = r'\,'
t_SCOL = r'\;'
def t_IF(t):
    r'if'
    return t
def t_ELSE(t):
    r'else'
    return t
def t_FOR(t): 
    r'for'
    return t
def t_WHILE(t):
    r'while'
    return t
def t_BREAK(t): 
    r'break'
    return t
def t_CONTINUE(t): 
    r'continue'
    return t
def t_RETURN(t):
    r'return'
    return t
def t_EYE(t):
    r'eye'
    return t
def t_ZEROS(t):
    r'zeros'
    return t
def t_ONES(t):
    r'ones'
    return t
def t_PRINT(t): 
    r'print'
    return t

literals = [ '+','-','*','/','(',')' ]

def t_FLOAT(t):
    r'((\d+\.\d*)|(\d*\.\d+))(E\d+)?'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t

def t_comment(t):
    r'\#[^\n]*'

def t_STRING(t):
    r'\"[^\"]*\"'
    return t

t_ignore = '  \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t) :
    print "Illegal character '%s'" %t.value[0]
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

lexer = lex.lex()
fh = open(sys.argv[1], "r")
file_content = fh.read()
lexer.input( file_content )
for token in lexer:
    print("line %d, column %d: %s(%s)" %(token.lineno, find_column(file_content, token), token.type, token.value))