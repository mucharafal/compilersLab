class Number():
    def __init__(self, value=0):
        self.value = value

    def getValue(self):
        return self.value

class Integer(Number):
    def __init__(self, value = 0):
        super().__init__(value)

class Float(Number):
    def __init__(self, value = 0):
        super().__init__(value)

class String():
    def __init__(self, value = ""):
        self.value = value

class Array():
    def __init__(self, elementTypes, size, values = []):
        self.elementTypes = elementTypes
        self.size = size
        self.values = values

class Matrix():
    def __init__(self, xSize, ySize, elementTypes, values = []):
        self.xSize = xSize
        self.ySize = ySize
        self.elementTypes = elementTypes
        self.values = values

    @staticmethod
    def areEqualSize(first, second):
        return first.xSize == second.xSize and \
            first.ySize == second.ySize

    @staticmethod
    def add(first, second):
        if areEqualSize(first, second):
            


class Boolean():
    def __init__(self, value = False):
        self.value = value

class Expression():
    pass

class Variable():
    def __init__(self, name = "", value = None):
        self.name = name
        self.value = value