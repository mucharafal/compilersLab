#!/usr/bin/python3

import scanner
import ply.yacc as yacc
import sys
from AST import *
from TreePrinter import *

tokens = scanner.tokens

precedence = (
   ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
   ("left", "*", "/", 'DOTMUL', 'DOTDIVIDE'),
   ("left", "TRANSPOSITION")
)

def p_program(p):
    """program : instructions"""
    p[0] = p[1]

def p_instructions(p):
    """instructions : instruction instructions 
    | instruction"""
    if len(p) == 2:
        p[0] = Block([p[1]])
    else:
        p[0] = p[2]
        p[2].body = [p[1]] + p[2].body

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
    if len(p) == 3:
        p[0] = Jump(p[1])
    else:
        p[0] = p[1]


def p_blockInstruction(p):
    """blockInstruction : '{' instructions '}'"""
    p[0] = p[2]
#string

def p_string(p):
    """string : STRING"""
    p[0] = String(p[1])

def p_stringExpression(p):
    """stringExpression : variable
    | string
    | stringExpression '+' stringExpression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinaryExpression(p[2], p[1], p[3])

#number

def p_int(p):
    """number : INT """
    p[0] = IntNum(p[1])

def p_float(p):
    """number : FLOAT"""
    p[0] = FloatNum(p[1])

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
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    elif p[1] == '-':
        p[0] = UnaryExpression(p[1], p[2])
    else:
        p[0] = BinaryExpression(p[2], p[1], p[3])

def p_arrayType(p):
    """arrayExpression : '[' row ']'
    | numberExpression ':' numberExpression
    | variable"""
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == ':':
        p[0] = Array.fromRange(p[1], p[3])
    else:
        p[0] = Array.fromList(p[2])

#matrix

def p_row(p):
    """row : number ',' row
    | number"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_rows(p):
    """rows : semicolonRows
    | bracketRows"""
    p[0] = p[1]

def p_semicolonRows(p):
    """semicolonRows : row ';' rows
    | row"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] +  p[3]

def p_bracketRows(p):
    """bracketRows : arrayExpression ',' bracketRows
    | arrayExpression"""
    if len(p) == 2:
        p[0] = [p[1].list]
    else:
        p[0] = [p[1].list] +  p[3]


def p_matrix(p):
    """matrix : '[' rows ']'
    | EYE '(' INT ')'
    | ZEROS '(' INT ')'
    | ONES '(' INT ')'"""
    if p[1] == '[':
        p[0] = Matrix(p[2])
    else:
        p[0] = Matrix((p[1], IntNum(p[3])))


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
        p[0] = UnaryExpression(p[2], p[1])
    else:
        p[0] = BinaryExpression(p[2], p[1], p[3])

def p_matrixType(p):
    """matrixType : matrix
    | variable
    | matrixExpression""" # or variable instead ID
    p[0] = p[1]

def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(file_content, p), p.type, p.value))
    else:
        print("Unexpected end of input")

#sum up
def p_variable(p):
    """variable : ID"""
    p[0] = Variable(p[1])
    
def p_reference(p):
    """reference : variable '[' numberExpression ']'
    | variable '[' numberExpression ',' numberExpression ']'"""
    if len(p) == 5:
        p[0] = Reference(p[1], [p[3]])
    else:
        p[0] = Reference(p[1], [p[3], p[5]])

def p_assignment(p):
    """assignment : variable '=' expression ';'
    | reference '=' expression ';'"""
    p[0] = BinaryExpression(p[2], p[1], p[3])

def p_operationAndAssignment(p):
    """operationAndAssignment : variable ASSPLUS expression ';'
    | variable ASSMINUS expression ';'
    | variable ASSMUL expression ';'
    | variable ASSDIVIDE expression ';'"""
    p[0] = BinaryExpression(p[2], p[1], p[3])

def p_if(p):
    """conditionInstruction : IF '(' logicalExpression ')' instruction ELSE instruction
    | IF '(' logicalExpression ')' instruction"""
    if len(p) == 6:
        p[0] = If(p[3], p[5])
    else:
        p[0] = Else(p[3], p[5], p[7])

def p_while(p):
    """whileLoopInstruction : WHILE '(' logicalExpression ')' instruction"""
    p[0] = While(p[3], p[5])

def p_for(p):
    """forLoopInstruction : FOR ID '=' arrayExpression instruction"""
    p[0] = For(Variable(p[2]), p[4], p[5])

def p_loopOperation(p):
    """loopInstruction : forLoopInstruction 
    | whileLoopInstruction"""
    p[0] = p[1]

def p_logicaloperator(p):
    """logicalOperator : LE 
                        | GE 
                        | NE 
                        | EQ 
                        | LT 
                        | GT"""
    p[0] = p[1]

def p_logicalexpression(p):
    """logicalExpression : numberExpression logicalOperator numberExpression"""
    p[0] = BinaryExpression(p[2], p[1], p[3])

def p_returnStatement(p):
    """returnStatement : RETURN numberExpression ';'"""
    p[0] = Return(p[2])

def p_printInstruction(p):
    """printInstruction : PRINT valuesToPrint ';'"""
    p[0] = Print(p[2])

def p_valuesToPrint(p):
    """valuesToPrint : expression ',' valuesToPrint
    | expression"""
    if len(p) == 2:
        p[0] = [p[1]]          #list
    else:
        p[0] = [p[1]] + p[3]

def p_expression(p):
    """expression : variable
    | logicalExpression
    | matrixType
    | numberExpression
    | stringExpression
    | arrayExpression
    | reference"""
    p[0] = p[1]


parser = yacc.yacc()
