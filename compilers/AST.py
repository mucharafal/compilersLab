class Node(object):
    pass

class ValueNode(Node):
    pass

class IntNum(ValueNode):
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column

class FloatNum(ValueNode):
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column

class String(ValueNode):
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column

class Matrix(Node):
    #expected that value is list
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column

class Array(Node):
    @staticmethod
    def fromRange(begin, end, line, column):
        return Array((begin, end), line, column)

    @staticmethod
    def fromList(contentList, line, column):
        return Array(contentList, line, column)

    def __init__(self, contentList, line, column):
        if isinstance(contentList, list):
            self.type = list
            self.list = contentList
        else:
            self.type = range
            self.boundary = contentList
        self.line = line
        self.column = column

class While(Node):
    def __init__(self, cond, body, line, column):
        self.cond = cond
        self.body = body
        self.line = line
        self.column = column

class For(Node):
    def __init__(self, var, arr, body, line, column):
        self.arr = arr
        self.body = body
        self.var = var
        self.line = line
        self.column = column

class If(Node):
    def __init__(self, cond, body, line, column):
        self.cond = cond
        self.body = body
        self.line = line
        self.column = column

class Else(Node):
    def __init__(self, cond, body1, body2, line, column):
        self.cond = cond
        self.body1 = body1
        self.body2 = body2
        self.line = line
        self.column = column

class Jump(Node):
    def __init__(self, type, line, column):
        self.type = type
        self.line = line
        self.column = column

class Variable(Node):
    def __init__(self, name, line, column):
        self.name = name
        self.line = line
        self.column = column

class Reference(Node):
    def __init__(self, variable, arguments, line, column):
        self.variable = variable
        self.arguments = arguments
        self.line = line
        self.column = column

class BinaryExpression(Node):
    def __init__(self, op, left, right, line, column):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        self.column = column


class UnaryExpression(Node):
    def __init__(self, op, left, line, column):
        self.op = op
        self.left = left
        self.line = line
        self.column = column

class Return(Node):
    def __init__(self, expr, line, column):
        self.expr = expr
        self.line = line
        self.column = column

class Print(Node):
    def __init__(self, val, line, column):
        self.val = val
        self.line = line
        self.column = column

class Block(Node):
    def __init__(self,body, line, column):
        self.body = body
        self.line = line
        self.column = column

class Error(Node):
    def __init__(self):
        pass
