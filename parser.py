#!/usr/bin/python

import scanner
import ply.yacc as yacc
import sys


tokens = scanner.tokens

precedence = (
   ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
   ("left", "*", "/", 'DOTMUL', 'DOTDIVIDE'),
   ("left", "TRANSPOSITION")
)

def p_program(p):
    """program : instructions"""
    print("p[1] = ", p[1])

def p_instructions(p):
    """instructions : instruction instructions 
    | instruction"""
    if len(p) == 2:
        p[0] = ('instructions', p[1])
    else:
        p[0] = ('instructions', p[1], p[2])

def p_instruction(p):
    """instruction : conditionInstruction
    | loopInstruction
    | BREAK ';'
    | CONTINUE ';'
    | returnStatement
    | assignment
    | operationAndAssignment
    | printInstruction
    | blockInstruction"""
    p[0] = ('instruction', p[1])

def p_blockInstruction(p):
    """blockInstruction : '{' instructions '}'"""
    p[0] = ('blockInstruction', p[2])
#string

def p_string(p):
    """string : STRING"""
    p[0] = ('string', p[1])

def p_stringExpression(p):
    """stringExpression : variable
    | string
    | stringExpression '+' stringExpression"""
    if len(p) == 2:
        p[0] = ('stringExpression', p[1])
    else:
        p[0] = ('stringExpression', p[2], p[1], p[3])

#number

def p_number(p):
    """number : INT 
    | FLOAT"""
    p[0] = ('number', p[1])

def p_numberExpression(p):
    """numberExpression : number
    | variable
    | '(' numberExpression ')'
    | numberExpression '+' numberExpression
    | numberExpression '-' numberExpression
    | numberExpression '*' numberExpression
    | numberExpression '/' numberExpression
    | '-' numberExpression"""
    if len(p) == 2:
        p[0] = ('numberExpression', p[1])
    elif p[1] == '(':
        p[0] = ('numberExpression', p[2])
    elif p[1] == '-':
        p[0] = ('numberExpression', p[1], p[2])
    else:
        p[0] = ('numberExpression', p[2], p[1], p[3])

def p_arrayType(p):
    """arrayExpression : '[' row ']'
    | numberExpression ':' numberExpression
    | variable"""
    if len(p) == 2:
        p[0] = ('arrayType', p[1])
    elif p[2] == ':':
        p[0] = ('arrayType', p[2], p[1], p[3])
    else:
        p[0] = ('arrayType', p[2])
#matrix

def p_row(p):
    """row : number ',' row
    | number"""
    if len(p) == 2:
        p[0] = ('row', p[1])
    else:
        p[0] = ('row', p[1], p[3])

def p_rows(p):
    """rows : semicolonRows
    | bracketRows"""
    p[0] = ('rows', p[1])

def p_semicolonRows(p):
    """semicolonRows : row ';' rows
    | row"""
    if len(p) == 2:
        p[0] = ('semicolonRows', p[1])
    else:
        p[0] = ('semicolonRows', p[1], p[3])

def p_bracketRows(p):
    """bracketRows : arrayExpression ',' bracketRows
    | arrayExpression"""
    if len(p) == 2:
        p[0] = ('bracketRows', p[1])
    else:
        p[0] = ('bracketRows', p[1], p[3])


def p_matrix(p):
    """matrix : '[' rows ']'
    | EYE '(' INT ')'
    | ZEROS '(' INT ')'
    | ONES '(' INT ')'"""
    if p[1] == '[':
        p[0] = ('matrix', p[2])
    else:
        p[0] = ('matrix', p[1], p[3])


def p_matrixExpression(p):
    """matrixExpression : matrixType '+' matrixType
    | matrixType '-' matrixType
    | matrixType '*' matrixType
    | matrixType '/' matrixType
    | matrixType DOTPLUS matrixType
    | matrixType DOTMINUS matrixType
    | matrixType DOTMUL matrixType
    | matrixType DOTDIVIDE matrixType
    | matrixType TRANSPOSITION"""
    if len(p) == 3:
        p[0] = ('matrixExpression', p[1])
    else:
        p[0] = ('matrixExpression', p[2], p[1], p[3])

def p_matrixType(p):
    """matrixType : matrix
    | variable
    | matrixExpression""" # or variable instead ID
    p[0] = ('matrixType', p[1])

def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(file_content, p), p.type, p.value))
    else:
        print("Unexpected end of input")


# def p_artihmetic(p):
#     """expression : expression '+' expression
#                   | expression '-' expression
#                   | expression '*' expression
#                   | expression '/' expression
#                   | '(' expression ')'
#                   | number
#                   | string
#                   | matrix"""
#     if p[1] == '('   : p[0] = p[2]
#     elif p[2] == '+' : p[0] = p[1] + p[3]
#     elif p[2] == '-' : p[0] = p[1] - p[3]               
#     elif p[2] == '*' : p[0] = p[1] * p[3]                         
#     elif p[2] == '/' : p[0] = p[1] / p[3]

#sum up
def p_variable(p):
    """variable : ID
    | ID '[' numberExpression ']'
    | ID '[' numberExpression ',' numberExpression ']'"""
    if len(p) == 2:
        p[0] = ('variable', p[1])
    elif len(p) == 5:
        p[0] = ('variable', p[1], p[3])
    else:
        p[0] = ('variable', p[1], p[3], p[5])

def p_assignment(p):
    """assignment : variable '=' expression ';'"""
    p[0] = ('assignment', p[1], p[3])

def p_operationAndAssignment(p):
    """operationAndAssignment : variable ASSPLUS expression ';'
    | variable ASSMINUS expression ';'
    | variable ASSMUL expression ';'
    | variable ASSDIVIDE expression ';'"""
    p[0] = ('operationAndAssignment', p[1], p[3])

def p_if(p):
    """conditionInstruction : IF '(' logicalExpression ')' instruction ELSE instruction
    | IF '(' logicalExpression ')' instruction"""
    if len(p) == 6:
        p[0] = ('conditionInstruction', p[3], p[5])
    else:
        p[0] = ('conditionInstrution', p[3], p[5], p[7])

def p_while(p):
    """whileLoopInstruction : WHILE '(' logicalExpression ')' instruction"""
    p[0] = ('whileLoopInstruction', p[3], p[5])

def p_for(p):
    """forLoopInstruction : FOR ID '=' arrayExpression instruction"""
    p[0] = ('forLoopInstruction', p[2], p[4], p[5])

def p_loopOperation(p):
    """loopInstruction : forLoopInstruction 
    | whileLoopInstruction"""
    p[0] = ('loopOperation', p[1])

def p_logicaloperator(p):
    """logicalOperator : LE 
                        | GE 
                        | NE 
                        | EQ 
                        | LT 
                        | GT"""
    p[0] = ('logicalOperator', p[1])

def p_logicalexpression(p):
    """logicalExpression : numberExpression logicalOperator numberExpression"""
    p[0] = ('logicalExpression', p[2], p[1], p[3])

def p_returnStatement(p):
    """returnStatement : RETURN numberExpression ';'"""
    p[0] = ('returnStatement', p[2])

def p_printInstruction(p):
    """printInstruction : PRINT valuesToPrint ';'"""
    p[0] = ('printInstruction', p[2])

def p_valuesToPrint(p):
    """valuesToPrint : expression ',' valuesToPrint
    | expression"""
    if len(p) == 2:
        p[0] = ('valuesToPrint', p[1])
    else:
        p[0] = ('valuesToPrint', p[1], p[3])

def p_expression(p):
    """expression : variable
    | logicalExpression
    | matrixType
    | numberExpression
    | stringExpression
    | arrayExpression"""
    p[0] = ('expression', p[1])


parser = yacc.yacc()
