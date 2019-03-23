#!/usr/bin/python

import scanner
import ply.yacc as yacc
import sys


tokens = scanner.tokens

precedence = (
   ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
   ("left", "*", "/", 'DOTMUL', 'DOTDIVIDE')
)

def p_program(p):
    """program : instructions"""

def p_instructions(p):
    """instructions : instruction instructions 
    | instruction"""

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

def p_blockInstruction(p):
    """blockInstruction : '{' instructions '}'"""

#string

def p_string(p):
    """string : STRING"""
    p[0] = p[1]

def p_stringExpression(p):
    """stringExpression : variable
    | string
    | stringExpression '+' stringExpression"""
    pass

#number

def p_number(p):
    """number : INT 
    | FLOAT"""
    # p[0] = p[1]

def p_numberExpression(p):
    """numberExpression : number
    | variable
    | '(' numberExpression ')'
    | numberExpression '+' numberExpression
    | numberExpression '-' numberExpression
    | numberExpression '*' numberExpression
    | numberExpression '/' numberExpression
    | '-' numberExpression"""
    pass

def p_arrayType(p):
    """arrayExpression : '[' row ']'
    | numberExpression ':' numberExpression
    | variable"""

#matrix

def p_row(p):
    """row : number ',' row
    | number"""
    # if p.length == 2:
    #     p[0] = [p[1]]
    # else:
    #     p[0] = [p[1]] + p[3]

def p_rows(p):
    """rows : semicolonRows
    | bracketRows
    semicolonRows : row ';' rows
    | row
    bracketRows : arrayExpression ',' bracketRows
    | arrayExpression"""
    # if p.length == 2:
    #     p[0] = [p[1]]
    # else:
    #     p[0] = [p[1]] + p[3]


def p_matrix(p):
    """matrix : '[' rows ']'
    | EYE '(' INT ')'
    | ZEROS '(' INT ')'
    | ONES '(' INT ')'"""
    # if p.length == 4:
    #     p[0] = p[2]
    # elif p[1] == 'eye':     #eye or EYE?
    #     pass
    # elif p[1] == 'zeros':
    #     pass
    # elif p[1] == 'ones':
    #     pass


def p_matrixExpression(p):
    """matrixExpression : matrixType '+' matrixType
    | matrixType '-' matrixType
    | matrixType '*' matrixType
    | matrixType '/' matrixType
    | matrixType DOTPLUS numberExpression
    | matrixType DOTMINUS numberExpression
    | matrixType DOTMUL numberExpression
    | matrixType DOTDIVIDE numberExpression
    | matrixType TRANSPOSITION"""

def p_matrixType(p):
    """matrixType : matrix
    | variable
    | matrixExpression""" # or variable instead ID
    pass

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

def p_assignment(p):
    """assignment : variable '=' expression ';'"""

def p_operationAndAssignment(p):
    """operationAndAssignment : variable ASSPLUS expression ';'
    | variable ASSMINUS expression ';'
    | variable ASSMUL expression ';'
    | variable ASSDIVIDE expression ';'"""
    pass

def p_if(p):
    """conditionInstruction : IF '(' logicalExpression ')' instruction ELSE instruction
    | IF '(' logicalExpression ')' instruction"""

def p_while(p):
    """whileLoopInstruction : WHILE '(' logicalExpression ')' instruction"""
    # p[0] = (p[2], p[4])

def p_for(p):
    """forLoopInstruction : FOR ID '=' arrayExpression instruction"""
    # p[0] = (p[2], p[4])

def p_loopOperation(p):
    """loopInstruction : forLoopInstruction 
    | whileLoopInstruction"""
    pass

def p_logicaloperator(p):
    """logicalOperator : LE 
                        | GE 
                        | NE 
                        | EQ 
                        | LT 
                        | GT"""

def p_logicalexpression(p):
    """logicalExpression : numberExpression logicalOperator numberExpression"""
    pass

def p_returnStatement(p):
    """returnStatement : RETURN numberExpression ';'"""

def p_printInstruction(p):
    """printInstruction : PRINT valuesToPrint ';'"""

def p_valuesToPrint(p):
    """valuesToPrint : expression ',' valuesToPrint
    | expression"""

def p_expression(p):
    """expression : variable
    | logicalExpression
    | matrixType
    | numberExpression
    | stringExpression
    | arrayExpression"""

if __name__ == '__main__':
    parser = yacc.yacc()
    fh = open(sys.argv[1], "r")
    file_content = fh.read()
    parser.parse(file_content, scanner.lexer)
    # for p in parser.token:
    #     print(p)
