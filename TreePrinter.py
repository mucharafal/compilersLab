from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @staticmethod
    def makeIndent(indent):
        return " | " * indent

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.ValueNode)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + str(self.value))


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        def printAsVector(potentialList, indentInner):
            print(TreePrinter.makeIndent(indentInner) + "Array")
            if isinstance(potentialList, list):
                for i in potentialList:
                    printAsVector(i, indentInner+1)
            elif isinstance(potentialList, AST.Node):
                potentialList.printTree(indentInner+1)
            else:
                print(TreePrinter.makeIndent(indentInner) + str(potentialList))
        printAsVector(self.value, indent)

    @addToClass(AST.Array)
    def printTree(self, indent=0):
        def printAsVector(potentialList, indentInner):
            print(TreePrinter.makeIndent(indentInner) + "Array")
            if isinstance(potentialList, list):
                for i in potentialList:
                    printAsVector(i, indentInner+1)
            elif isinstance(potentialList, AST.Node):
                potentialList.printTree(indentInner+1)
            else:
                print(TreePrinter.makeIndent(indentInner) + str(potentialList))

        printAsVector(self.list)

    @addToClass(AST.BinaryExpression)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "While")
        self.cond.printTree(indent+1)
        self.body.printTree(indent+1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "For")
        self.var.printTree(indent+1)
        self.arr.printTree(indent+1)
        self.body.printTree(indent+1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "If")
        self.cond.printTree(indent+1)
        print(TreePrinter.makeIndent(indent) + "Then")
        self.body.printTree(indent+1)

    @addToClass(AST.Else)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "If")
        self.cond.printTree(indent+1)
        print(TreePrinter.makeIndent(indent) + "Then")
        self.body1.printTree(indent+1)
        print(TreePrinter.makeIndent(indent) + "Else")
        self.body2.printTree(indent+1)

    @addToClass(AST.Jump)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.type)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.name)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "Reference")
        self.variable.printTree(indent+1)
        for i in self.arguments:
            i.printTree(indent+1)

    @addToClass(AST.UnaryExpression)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.op)
        self.left.printTree(indent+1)
        
    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "Return")
        self.expr.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "Print")
        for i in self.val:
            i.printTree(indent+1)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for i in self.body:
            i.printTree(indent)


# condition = AST.BinaryExpression("<", AST.IntNum(10), AST.IntNum(12))
# p = AST.While(condition, condition)
# p.printTree()