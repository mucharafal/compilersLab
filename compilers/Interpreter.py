
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
        return type(matrix) is Matrix or type(matrix) is Array

    @staticmethod
    def wrapNumber(number):
        return Number.wrap(number)

    @staticmethod
    def wrapMatrix(rawMatrix):
        x = len(rawMatrix)
        y = len(rawMatrix[0]) 
        matrixType = type(rawMatrix[0][0])
        return Matrix(x, y, matrixType, rawMatrix)

    @staticmethod
    def wrapArray(rawArray):
        x = len(rawArray)
        arrayType = type(rawArray[0])
        return Array(arrayType, x, rawArray)

    @on('node')
    def visit(self, node):
        print("CO to")
        print(node)
        pass

    @when(AST.BinaryExpression)
    def visit(self, node):
        print("Interpret bin expr")
        left = node.left.accept(self)
        right = node.right.accept(self)
        operator = node.op
        numberOperation = { 
            '+': lambda x, y: Number.wrap(x + y),
            '-': lambda x, y: Number.wrap(x - y),
            '*': lambda x, y: Number.wrap(x * y),
            '/': lambda x, y: Number.wrap(x / y)
        }
        matrixOperation = {
            '+': lambda x, y: Matrix.add(x, y),
            '-': lambda x, y: Matrix.substract(x, y),
            '*': lambda x, y: Matrix.multiply(x, y),
            '/': lambda x, y: Matrix.divide(x, y)
        }
        matrixDotOperation = {
            '.+': lambda x, y: Matrix.add(x, y),
            '.-': lambda x, y: Matrix.substract(x, y),
            '.*': lambda x, y: Matrix.multiplyElementWise(x, y),
            './': lambda x, y: Matrix.divide(x, y)
        }
        booleanOperation = {
            '<': lambda x, y: Boolean.less(x,y),
            '>': lambda x, y: Boolean.greater(x, y),
            '<=': lambda x, y: Boolean.lessEqual(x, y),
            '>=': lambda x, y: Boolean.greaterEqual(x, y),
            '==': lambda x, y: Boolean.equal(x, y),
            '!=': lambda x, y: Boolean.notEqual(x, y)
        }
        if operator in ['+', '-', '*', '/']:
            if Interpreter.isNumber(left):
                return numberOperation[operator](left, right)
            elif Interpreter.isMatrix(left):
                return matrixOperation[operator](left, right)
        if operator in ['+=', '-=', '*=', '/=']:
            if Interpreter.isNumber(left):
                value = numberOperation[operator[0]](left, right)
                self.memory.set(node.left.name, value)
                return value
            elif Interpreter.isMatrix(left):
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
            if isinstance(node.left, AST.Reference):
                var = node.left.variable.accept(self)
                if isinstance(var, Matrix) and len(node.left.arguments) == 2:
                    arg1 = node.left.arguments[0].accept(self)
                    arg2 = node.left.arguments[1].accept(self)
                    if var.elementTypes is type(right):
                        var.values[arg1.value][arg2.value] = right
                    else:
                        raise TypeError()
                else:
                    arg1 = node.left.arguments[0].accept(self)
                    if var.elementTypes is type(right):
                        var.values[arg1.value] = right
                    else:
                        raise TypeError()

            else:
                self.memory.insert(node.left.name, right)
            return right


    @when(AST.UnaryExpression)
    def visit(self, node):
        r1 = node.left.accept(self)
        print(r1)
        op = node.op
        if op == '-':
            if Interpreter.isNumber(r1):
                return Number.wrap(r1.value * -1)
            elif Interpreter.isMatrix(r1):
                for i in range(r1.xSize):
                    for j in range(r1.ySize):
                        r1.values[i][j] = -r1.values[i][j] 
            else:
                raise TypeError()
        if op == '\'':
            if Interpreter.isMatrix(r1):
                return Matrix.transpose(r1)
            else:
                raise TypeError()
    

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
        if type(node.value) is tuple:
            functionName = node.value[0]
            size = node.value[1]
            size = size.accept(self)
            if functionName == "zeros":
                result = [[Number.wrap(0)] * size.value] * size.value
                return Matrix(len(result), len(result[0]), type(result[0][0]), result)
            if functionName == "ones":
                result = [[Number.wrap(1)] * size.value] * size.value
                return Matrix(len(result), len(result[0]), type(result[0][0]), result)
            if functionName == "eye":
                result = []
                for i in range(size.value):
                    row = [Number.wrap(0)] * i + [Number.wrap(1)] + [Number.wrap(0)] * (size.value - i - 1)
                    result = result + [row]
                return Matrix(len(result), len(result[0]), type(result[0][0]), result)
            
        else:
            result = []
            for row in node.value:
                temp = []
                for element in row:
                    value = element.accept(self)
                    temp = temp + [value]
                result = result + [temp]
            return Matrix(len(result), len(result[0]), type(result[0][0]), result)

    @when(AST.Array)
    def visit(self, node):
        node.value.accept(self)
        return wrapArray(node.value)

    @when(AST.While)
    def visit(self, node):
        result = None
        try:
            while node.cond.accept(self).value:
                try:
                    result = node.body.accept(self)
                except ContinueException:
                    pass
        except BreakException:
            pass
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
        if node.cond.accept(self).value:
            return node.body.accept(self)

    @when(AST.Else)
    def visit(self, node):
        if node.cond.accept(self).value:
            return node.body1.accept(self)
        else:
            return node.body2.accept(self)

    @when(AST.Jump)
    def visit(self, node):
        if node.type =="break":
            raise BreakException()
        else:
            raise ContinueException

    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(AST.Reference)
    def visit(self, node):
        var = node.variable.accept(self)
        if isinstance(var, Matrix) and len(node.arguments) == 2:
            arg1 = node.arguments[0].accept(self)
            arg2 = node.arguments[1].accept(self)
            return var.values[arg1.value][arg2.value]
        else:
            arg1 = node.arguments[0].accept(self)
            return var.values[arg1.value]

    @when(AST.Print)
    def visit(self, node):
        values = node.val
        listValues = []
        for value in values:
            listValues = listValues + [value.accept(self)]
    
        for value in listValues:
            valType = type(value)
            if valType is Integer or valType is Float or valType is String:
                return print(value.value)
            elif valType is Matrix or valType is Array:
                return print(value.toString())
            else:
                raise TypeError(valType)

    @when(AST.IntNum)
    def visit(self, node):
        number = Number.wrap(node.value)
        return number

    @when(AST.ValueNode)
    def visit(self, node):
        return node.accept(self)

    @when(AST.FloatNum)
    def visit(self, node):
        return Number.wrap(node.value)

    @when(AST.String)
    def visit(self, node):
        return String(node.value)
