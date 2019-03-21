#!/usr/bin/python

import scanner
import ply.yacc as yacc


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
<<<<<<< HEAD
    | BREAK ';'
    | CONTINUE ';'
=======
    | BREAK
    | CONTINUE
>>>>>>> aa0e83ac04d2fadc07a39a09cd758b832140c4dc
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

def p_stringAssignment(p):
    """stringAssignment : ID '=' stringExpression ';'"""
    pass

def p_stringExpression(p):
    """stringExpression : ID
    | string
    | stringExpression '+' stringExpression"""
    pass

#number

def p_number(p):
    """number : INT 
    | FLOAT"""
    p[0] = p[1]

def p_numberAssignment(p):
    """numberAssignment : ID '=' numberExpression ';'"""

def p_numberExpression(p):
    """numberExpression : number
    | ID
    | '(' numberExpression ')'
    | numberExpression '+' numberExpression
    | numberExpression '-' numberExpression
    | numberExpression '*' numberExpression
    | numberExpression '/' numberExpression
    | '-' numberExpression"""
    pass

#matrix

def p_row(p):
    """row : number ',' row
    | number"""
    if p.length == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_rows(p):
    """rows : row ';' rows
    | row"""
    if p.length == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_matrix(p):
    """matrix : '[' rows ']'
    | EYE '(' INT ')'
    | ZEROS '(' INT ')'
    | ONES '(' INT ')'"""
    if p.length == 4:
        p[0] = p[2]
    elif p[1] == 'eye':     #eye or EYE?
        pass
    elif p[1] == 'zeros':
        pass
    elif p[1] == 'ones':
        pass

def p_matrixAssignment(p):
    """matrixAssignment : ID '=' matrixExpression ';'"""

def p_matrixExpression(p):
    """matrixExpression : matrixType '+' matrixType
    | matrixType '-' matrixType
    | matrixType '*' matrixType
    | matrixType '/' matrixType
    | matrixType DOTPLUS numberExpression
    | matrixType DOTMINUS numberExpression
    | matrixType DOTMUL numberExpression
    | matrixType DOTDIVIDE numberExpression"""

def p_matrixType(p):
    """matrixType : matrix
    | ID
    | matrixExpression"""
    pass

def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p), p.type, p.value))
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
def p_assignment(p):
    """assignment : stringAssignment
    | numberAssignment
    | matrixAssignment"""

def p_operationAndAssignment(p):
<<<<<<< HEAD
    """operationAndAssignment : ID ASSPLUS value ';'
    | ID ASSMINUS value ';'
    | ID ASSMUL value ';'
    | ID ASSDIVIDE value ';'"""
=======
    """operationAndAssignment : ID ASSPLUS value
    | ID ASSMINUS value
    | ID ASSMUL value
    | ID ASSDIVIDE value"""
>>>>>>> aa0e83ac04d2fadc07a39a09cd758b832140c4dc
    pass


def p_if(p):
    """conditionInstruction : IF logicalExpression instruction ELSE instruction
    | IF logicalExpression instruction"""

def p_while(p):
    """whileLoopInstruction : WHILE logicalExpression instruction"""
    p[0] = (p[2], p[4])

def p_for(p):
    """forLoopInstruction : FOR logicalExpression instruction"""
    p[0] = (p[2], p[4])

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
    pass

def p_logicalexpression(p):
    """logicalExpression : number logicalOperator number"""
    pass

def p_returnStatement(p):
<<<<<<< HEAD
    """returnStatement : RETURN number ';'"""

def p_printInstruction(p):
    """printInstruction : PRINT value ';'"""
=======
    """returnStatement : RETURN number"""

def p_printInstruction(p):
    """printInstruction : PRINT value"""
>>>>>>> aa0e83ac04d2fadc07a39a09cd758b832140c4dc

def p_value(p):
    """value : matrixType
    | numberExpression
    | stringExpression"""

parser = yacc.yacc()