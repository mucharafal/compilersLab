import Exceptions

class Number():
    def __init__(self, value=0):
        self.value = value

    def toString(self):
        return str(self.value)

    @staticmethod
    def wrap(value):
        return Integer(value) if type(value) is int else Float(value)

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

    def toString(self):
        return self.value

class Array():
    def __init__(self, elementTypes, size, values = []):
        self.elementTypes = elementTypes
        self.size = size
        self.values = values

    def toString(self):
        temp = []
        for el in row:
            temp = temp + [el.toString()]
        return str(temp)

class Matrix():
    def __init__(self, xSize, ySize, elementTypes, values = []):
        self.xSize = xSize
        self.ySize = ySize
        self.elementTypes = elementTypes
        self.values = values

    def toString(self):
        res = []
        for row in self.values:
            temp = []
            for el in row:
                temp = temp + [el.toString()]
            res = res + [temp]
        return str(res)

    @staticmethod
    def areEqualSize(first, second):
        return first.xSize == second.xSize and \
            first.ySize == second.ySize

    @staticmethod
    def add(first, second):
        if Matrix.areEqualSize(first, second):
            resultRaw = []
            for i in range(first.xSize):
                temp = []
                for j in range(first.ySize):
                    element = first.values[i][j].value + second.values[i][j].value
                    element = Number.wrap(element)
                    temp = temp + [element]
                resultRaw = resultRaw + [temp]
            return Matrix(first.xSize, first.ySize, type(resultRaw[0][0]), resultRaw)
        else:
            raise Exceptions.MatrixIncompatibleException()
    
    @staticmethod
    def substract(first, second):
        if Matrix.areEqualSize(first, second):
            resultRaw = []
            for i in range(first.xSize):
                temp = []
                for j in range(first.ySize):
                    element = first.values[i][j].value - second.values[i][j].value
                    element = Number.wrap(element)
                    temp = temp + [element]
                resultRaw = resultRaw + [temp]
            return Matrix(first.xSize, first.ySize, type(resultRaw[0][0]), resultRaw)
        else:
            raise Exceptions.MatrixIncompatibleException()

    @staticmethod
    def multiplyElementWise(first, second):
        if Matrix.areEqualSize(first, second):
            resultRaw = []
            for i in range(first.xSize):
                temp = []
                for j in range(first.ySize):
                    element = first.values[i][j].value * second.values[i][j].value
                    element = Number.wrap(element)
                    temp = temp + [element]
                resultRaw = resultRaw + [temp]
            return Matrix(first.xSize, first.ySize, type(resultRaw[0][0]), resultRaw)
        else:
            raise Exceptions.MatrixIncompatibleException()
    
    @staticmethod
    def divide(first, second):
        if Matrix.areEqualSize(first, second):
            resultRaw = []
            for i in range(first.xSize):
                temp = []
                for j in range(first.ySize):
                    element = first.values[i][j].value / second.values[i][j].value
                    element = Number.wrap(element)
                    temp = temp + [element]
                resultRaw = resultRaw + [temp]
            return Matrix(first.xSize, first.ySize, type(resultRaw[0][0]), resultRaw)
        else:
            raise Exceptions.MatrixIncompatibleException()

    @staticmethod
    def multiply(first, second):
        if first.ySize == second.xSize:
            resultRaw = []
            for i in range(first.xSize):
                temp = []
                for j in range(second.ySize):
                    element = 0
                    for k in range(first.ySize):
                        element = first.values[i][k].value * second.values[k][j].value

                    element = Number.wrap(element)
                    temp = temp + [element]
                resultRaw = resultRaw + [temp]
            return Matrix(first.ySize, second.ySize, type(resultRaw[0][0]), resultRaw)
        else:
            raise Exceptions.MatrixIncompatibleException()

    @staticmethod
    def transpose(x):
        result = []
        for j in range(x.ySize):
            raw = []
            for i in range(x.xSize):
                raw = raw + [x.values[i][j]]
            result = result + [raw]
        return Matrix(x.ySize, x.xSize, type(result[0][0]), result)

class Boolean():
    def __init__(self, value = False):
        self.value = value

    @staticmethod
    def less(x, y):
        return Boolean(x.value < y.value)

    @staticmethod
    def lessEqual(x, y):
        return Boolean(x.value <= y.value)

    @staticmethod
    def greater(x, y):
        return Boolean(x.value > y.value)

    @staticmethod
    def greaterEqual(x, y):
        return Boolean(x.value >= y.value)

    @staticmethod
    def equal(x, y):
        return Boolean(x.value == y.value)

    @staticmethod
    def notEqual(x, y):
        return Boolean(x.value != y.value)

class Expression():
    pass

class Variable():
    def __init__(self, name = "", value = None):
        self.name = name
        self.value = value