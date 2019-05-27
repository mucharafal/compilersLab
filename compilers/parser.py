#!/usr/bin/python3

import scanner
import ply.yacc as yacc
import sys
from AST import *
from TreePrinter import *

tokens = scanner.tokens

precedence = (
   ("left", "LT", "GT", 'LE', 'GE', 'NE', 'EQ'),
   ("left", "=", "ASSPLUS", 'ASSMINUS', 'ASSMUL', 'ASSDIVIDE'),
   ("left", ':'),
   ('left', 'DOTPLUS', 'DOTMINUS', 'DOTMUL', 'DOTDIVIDE'),
   ("left", '+', '-'),
   ("left", "*", "/"),
   ("left", "TRANSPOSITION")
)

def p_program(p):
    """program : instructions"""
    p[0] = p[1]

def p_instructions(p):
    """instructions : instruction instructions 
    | instruction """
    if len(p) == 2:
        p[0] = Block([p[1]], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    else:
        p[0] = p[2]
        p[2].body = [p[1]] + p[2].body

def p_instruction(p):
    """instruction : conditionInstruction
    | loopInstruction 
    | instructionWSC ';'
    | blockInstruction
    """
    p[0] = p[1]

def p_instructionWithSemicolon(p):
    """instructionWSC : jump
    | returnStatement
    | expression
    | printInstruction"""
    p[0] = p[1]

def p_jump(p):
    """jump : CONTINUE
    | BREAK"""
    p[0] = Jump(p[1], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_blockInstruction(p):
    """blockInstruction : '{' instructions '}'"""
    p[0] = p[2]
#string

def p_string(p):
    """string : STRING"""
    p[0] = String(p[1], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

#number

def p_int(p):
    """number : INT """
    p[0] = IntNum(p[1], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_float(p):
    """number : FLOAT"""
    p[0] = FloatNum(p[1], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_matrix(p):
    """matrix : '[' rows ']'
    | EYE '(' expression ')'
    | ZEROS '(' expression ')'
    | ONES '(' expression ')'"""
    if p[1] == '[':
        p[0] = Matrix(p[2], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    else:
        p[0] = Matrix((p[1], p[3]), p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

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
    """bracketRows : array ',' bracketRows
    | expression"""
    if len(p) == 2:
        p[0] = [p[1].list]
    else:
        p[0] = [p[1].list] +  p[3]

def p_arrayType(p):
    """array : '[' row ']'
    | expression ':' expression"""
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == ':':
        p[0] = Array.fromRange(p[1], p[3], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    else:
        p[0] = Array.fromList(p[2], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p), p.type, p.value))
    else:
        print("Unexpected end of input")

#sum up
def p_variable(p):
    """variable : ID"""
    p[0] = Variable(p[1], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    
def p_reference(p):
    """reference : variable '[' expression ']'
    | variable '[' expression ',' expression ']'"""
    if len(p) == 5:
        p[0] = Reference(p[1], [p[3]], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    else:
        p[0] = Reference(p[1], [p[3], p[5]], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_if(p):
    """conditionInstruction : IF '(' expression ')' instruction ELSE instruction
    | IF '(' expression ')' instruction"""
    if len(p) == 6:
        p[0] = If(p[3], p[5], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    else:
        p[0] = Else(p[3], p[5], p[7], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_while(p):
    """whileLoopInstruction : WHILE '(' expression ')' instruction"""
    p[0] = While(p[3], p[5], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_for(p):
    """forLoopInstruction : FOR ID '=' array instruction"""
    p[0] = For(Variable(p[2], line = p.lineno if type(p.lineno) is int else p.lexer.lineno, column = scanner.find_column(file_content, p)), p[4], p[5], line = p.lineno if type(p.lineno) is int else p.lexer.lineno, column = scanner.find_column(file_content, p))

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

def p_returnStatement(p):
    """returnStatement : RETURN expression """
    p[0] = Return(p[2], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_printInstruction(p):
    """printInstruction : PRINT valuesToPrint """
    p[0] = Print(p[2], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_valuesToPrint(p):
    """valuesToPrint : expression ',' valuesToPrint
    | expression"""
    if len(p) == 2:
        p[0] = [p[1]]          #list
    else:
        p[0] = [p[1]] + p[3]

def p_expression(p):
    """expression : variable
    | matrix
    | number
    | string
    | array
    | reference
    | binaryExpression
    | unaryExpression
    | '(' expression ')'"""
    p[0] = p[1]

def p_binaryOperator(p):
    """binaryOperator : logicalOperator
    | arithmeticOperator
    | assignmentOperator
    | elementwiseOperator"""
    p[0] = p[1]

def p_artihmeticOperator(p):
    """arithmeticOperator : '+'
    | '-'
    | '*'
    | '/' """
    p[0] = p[1]

def p_assignmentOperator(p):
    """assignmentOperator : '='
    | ASSPLUS
    | ASSMINUS 
    | ASSMUL 
    | ASSDIVIDE """
    p[0] = p[1]

def p_elementwiseOperator(p):
    """elementwiseOperator : DOTPLUS
    | DOTMINUS
    | DOTMUL 
    | DOTDIVIDE """
    p[0] = p[1]

def p_binaryExpression(p):
    """binaryExpression : expression binaryOperator expression"""
    p[0] = BinaryExpression(p[2], p[1], p[3], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

def p_unaryExpression(p):
    """unaryExpression : '-' expression
    | expression TRANSPOSITION """
    if(p[2] == '\''):
        p[0] = UnaryExpression(p[2], p[1], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))
    else:
        p[0] = UnaryExpression(p[1], p[2], p.lineno if type(p.lineno) is int else p.lexer.lineno, scanner.find_column(file_content, p))

parser = yacc.yacc()
