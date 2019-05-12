
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
from myTypes import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack(Memory("global"))

    @staticmethod
    def isNumber(number):
        return number is Number

    @staticmethod
    def isMatrix(matrix):
        return matrix is Matrix or matrix is Array

    @staticmethod
    def wrapNumber(number):
        return Integer(number) if number is int else Float(number)

    @staticmethod
    def wrapMatrix(rawMatrix):
        x = len(rawMatrix)
        y = len(rawMatrix[0]) 
        matrixType = type(rawMatrix[0][0])
        return Matrix(x, y, matrixType, rawMatrix)

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinaryExpression)
    def visit(self, node):
        print("Interpret bin expr")
        left = node.left.accept(self)
        right = node.right.accept(self)
        operator = node.op
        numberOperation = { 
            '+': lambda x, y: wrapNumber(x + y),
            '-': lambda x, y: wrapNumber(x - y),
            '*': lambda x, y: wrapNumber(x * y),
            '/': lambda x, y: wrapNumber(x / y)
        }
        matrixOperation = {
            '+': lambda x, y: #define this operation in Matrix class in myTypes
        }
        if operator in ['+', '-', '*', '/']:
            if isNumber(left):
                return numberOperation[operator](left, right)
            elif isMatrix(left):
                return matrixOperation[operator](left, right)
        if operator in ['+=', '-=', '*=', '/=']:
            if isNumber(left):
                value = numberOperation[operator[0]](left, right)
                self.memory.set(node.left.name, value)
                return value
            elif isMatrix(left):
                value = matrixOperation[operator[0]](left, right)
                self.memory.set(node.left.name, value)
                return value
            else:
                #string or array? what then?
                pass
        if operator in ['.+', '.-', '.*', './']:
            value = matrixDotOperation[operator](left, right)
            return value
        if operator in ['==', '<', '>', '<=', '>=', '!=']:
            return booleanOperation[operator](left, right)
        if operator == '=':
            self.memory.insert(node.left.name, right)
            return right
        

    @when(AST.UnaryExpression)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.op
        pass

    @when(AST.Return)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.op
        pass

    @when(AST.Block)
    def visit(self, node):
        print("Interpret block")
        for expression in node.body:
            expression.accept(self)

    @when(AST.Matrix)
    def visit(self, node):

    @when(AST.Array)
    def visit(self, node):

    @when(AST.While)
    def visit(self, node):
        result = None
        while node.cond.accept(self):
            result = node.while_block.accept(self)
        return result

    @when(AST.For)
    def visit(self, node):
        result = None
        for i in node.range.accept(self):
            self.memory_stack.insert(node.id, i)
            result = node.for_block.accept(self)
        return result

    @when(AST.If)
    def visit(self, node):
        if node.cond.accept(self):
            return node.if_block.accept(self)

    @when(AST.Else)
    def visit(self, node):
        if node.cond.accept(self):
            return node.if_block.accept(self)
        else:
            if node.else_block:
                return node.else_block.accept(self)

    @when(AST.Jump)
    def visit(self, node):
        if node.type =="break":
            raise BreakException()
        else
            raise ContinueException

    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(AST.Reference)
    def visit(self, node):
        return self.memory.get(node.name[node.arguments])

    @when(AST.Print)
    def visit(self, node):
        return print(node.val)



        



