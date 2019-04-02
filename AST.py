class Node(object):
    pass

class ValueNode(Node):
    pass

class IntNum(ValueNode):
    def __init__(self, value):
        self.value = value

class FloatNum(ValueNode):
    def __init__(self, value):
        self.value = value

class String(ValueNode):
    def __init__(self, value):
        self.value = value

class Matrix(Node):
    #expected that value is list
    def __init__(self, value):
        self.value = value

class Array(Node):
    @staticmethod
    def fromRange(begin, end):
        return Array((begin, end))

    @staticmethod
    def fromList(contentList):
        return Array(contentList)

    def __init__(self, contentList):
        if isinstance(contentList, list):
            self.type = list
            self.list = contentList
        else:
            self.type = range
            self.boundary = contentList

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For(Node):
    def __init__(self, var, arr, body):
        self.arr = arr
        self.body = body
        self.var = var

class If(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class Else(Node):
    def __init__(self, cond, body1, body2):
        self.cond = cond
        self.body1 = body1
        self.body2 = body2

class Jump(Node):
    def __init__(self, type):
        self.type = type

class Variable(Node):
    def __init__(self, name):
        self.name = name

class Reference(Node):
    def __init__(self, variable, arguments):
        self.variable = variable
        self.arguments = arguments

class BinaryExpression(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryExpression(Node):
    def __init__(self, op, left):
        self.op = op
        self.left = left

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

class Print(Node):
    def __init__(self, val):
        self.val = val

class Block(Node):
    def __init__(self,body):
        self.body = body


class Error(Node):
    def __init__(self):
        pass
