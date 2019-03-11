#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
   ("left", '+', '-', '.+', '.-'),
   ("left", "*", "/", '.*', './')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_artihmetic(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIVIDE expression"""
    if p[2] == '+'   : p[0] = p[1] + p[3]
    elif p[2] == '-' : p[0] = p[1] - p[3]               
    elif p[2] == '*' : p[0] = p[1] * p[3]                         
    elif p[2] == '/' : p[0] = p[1] / p[3]

def p_if(p):
    """operation : IF logicalExpression LBR operations RBR ELSE LBR operations RBR 
    | IF logicalExpression LBR operations RBR"""
    if p.length > 6:
        if p[2]: 
            p[0] = p[4] 
        else: 
            p[0] = p[8]
    else:
        if p[2]: p[0] = p[4]

def p_number(p):
    """number : INT | FLOAT"""
    p[0] = p[1]

def p_string(p):
    """string: STRING"""
    p[0] = p[1]

def p_while(p):
    """whileLoopOperation : WHILE logicalExpression LBR inLoopOperations RBR"""
    p[0] = (p[2], p[4])

def p_for(p):
    """forLoopOperation: FOR logicalExpression LBR inLoopOperations RBR"""
    p[0] = (p[2], p[4])

def p_loopOperation(p):
    """loopOperation: forLoopOperation | whileLoopOperation"""
    pass

def p_inLoopOperation(p):
    """inLoopOperation: operation | BREAK | CONTINUE"""
    pass

def p_inLoopOperations(p):
    """inLoopOperations: """

# to finish the grammar
# ....


    


parser = yacc.yacc()
