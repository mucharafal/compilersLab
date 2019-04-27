class Number():
    pass

class Integer(Number):
    pass

class Float(Number):
    pass

class String():
    pass

class Array():
    def __init__(self, elementTypes, size):
        self.elementTypes = elementTypes
        self.size = size

class Matrix():
    def __init__(self, xSize, ySize, elementTypes):
        self.xSize = xSize
        self.ySize = ySize
        self.elementTypes = elementTypes

class Boolean():
    pass

class Expression():
    pass

class Variable():
    pass