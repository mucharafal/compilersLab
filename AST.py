class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Matrix(Node):
    def __init__(self, value):
        self.value = value

class Array(Node):
    def __init__(self, value):
        self.value = value

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For(Node):
    def __init__(self, arr, body, var):
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


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryExpr(Node):
    def __init__(self, left, op):
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
