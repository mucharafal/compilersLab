#!/usr/bin/python3

import AST
from myTypes import *
from SymbolTable import *

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)



class TypeChecker(NodeVisitor):  

    def printPlace(self, node):
        self.wasError = True
        print("Problem in line: " + str(node.line) + ", column: " + str(node.column))

    def __init__(self):
        self.symbol_table = SymbolTable(None, "main")
        self.wasError = False

    def visit_BinaryExpression(self, node):
        op    = node.op
        left = node.left
        right = node.right   
        type1 = self.visit(left)
        type2 = self.visit(right)
        
        def artihmeticAllowed(type1, type2, operation):
            return isinstance(type1, (Integer, Float)) and isinstance(type2, (Integer, Float)) or \
                isinstance(type1, Matrix) and isinstance(type2, Matrix) or \
                    isinstance(type1, String) and isinstance(type2, String) and operation == '+'

        #assignment
        if op == '=':
            if isinstance(left, (AST.Variable)):
                self.symbol_table.put(left.name, VariableSymbol(left.name, type2))
                return type2
            elif isinstance(left, AST.Reference):
                if not type(type1) is type(type2):
                    self.printPlace(node)
                    self.wasError = True
                    print("Assignment with bad type in reference" + str(type1) + str(type2))
            else:
                self.printPlace(node)
                self.wasError = True
                print("Assignment to nonvariable")
        #operation and assignment
        elif op == '+=' or op == '-=' or op == '*=' or op == '/=':
            if isinstance(left, AST.Variable):
                if type(type1) == Variable:
                    self.printPlace(node)
                    self.wasError = True
                    print("Trying to operate on unassignment variable")
                elif artihmeticAllowed(type1, type2, op[0]):
                    return type1
                else:
                    self.printPlace(node)
                    print("Types in operation are wrong")
            else:
                self.printPlace(node)
                print("Assignment to nonvariable")
        #matrix operations
        elif op == '.+' or op == '.-' or op == '.*' or op == './':
            if type(type1) is type(type2) and isinstance(type1, Matrix):
                return type1
            else:
                self.printPlace(node)
                print("Incorrect types in operation " + op)
        #number operations
        elif op in ['+','-','*','/']:
            if artihmeticAllowed(type1, type2, op):
                return type1 if not isinstance(type2, Float) else type2
            else:
                self.printPlace(node)
                print("Incorrect types in operation " + op)
        #boolean or logical operations
        elif op in ['<', '>', '<=', '>=', '!=', '==']:
            if isinstance(type1, (Integer, Float)) and isinstance(type2, (Integer, Float)):
                return Boolean()
            else:
                self.printPlace(node)
                print("Trying to compare diffrent types:" + str(type1) + ";" + str(type2))
        else:
            self.printPlace(node)
            print("Unexprected binary expression...")
        return None

 

    def visit_Variable(self, node):
        #return object Varible()- what means, that variable is unbounded
        #or type of variable
        symbol = self.symbol_table.get(node.name)
        if symbol == None:
            return Variable()
        else:
            return symbol.type
    
    def visit_IntNum(self, node):
        return Integer()

    def visit_FloatNum(self, node):
        return Float()

    def visit_String(self, node):
        return String()

    def visit_UnaryExpression(self, node):
        type1 = self.visit(node.left)
        if node.op == '\'':
            if isinstance(type1, Matrix):
                return Matrix(type1.ySize, type1.xSize, type1.elementTypes)
            else:
                self.printPlace(node)
                print("Transposition on bad type:" + str(type1))
                return None
        if type(type1) is Integer or type(type1) is Float or type(type1) is Matrix:
            return type1
        self.printPlace(node)
        print("Unary operation on bad type: " + node.op + ";" + str(type1))
        return None
    
    def visit_Array(self, node):
        if node.type == range:
            return Array(Integer(), 0)
        else:
            content = node.contentList
            array_size = len(content)
            array_type = None
            if array_size == 0:
                array_type = None
            else:
                head, *tail = content
                type1 = self.visit(head)
                array_type = type1
                for element in tail:
                    if not type(type1) is type(self.visit(element)):
                        self.printPlace(node)
                        print("Inconsistent types in array")
            return Array(array_type, array_size)

    def visit_Matrix(self, node):
        content = node.value
        if isinstance(content, tuple):
            #function
            functionName, sizeObj = content
            size = sizeObj.value
            type_of_size = self.visit(sizeObj)
            if not isinstance(type_of_size, Integer):
                self.printPlace(node)
                print("Incorrect argument of function: " + functionName)
                return None
            else:
                return Matrix(size, size, Integer())
        #check types and size
        head, *tail = content
        head_type = self.visit(head)
        for element in tail:
            element_type = self.visit(element)
            if not type(head_type.elementTypes) is type(element_type.elementTypes):
                self.printPlace(node)
                print("Type of arrays in matrix is inconsistent")
            if not head_type.size == element_type.size:
                self.printPlace(node)
                print("Size of arrays in matrix is inconsistent")
        return Matrix(len(content), head_type.size, head_type.elementTypes)

    def visit_While(self, node):
        type_of_cond = self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope("loop")             #loop is new scope for variables
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()                    #get old variable scope
        if not isinstance(type_of_cond, Boolean):
            self.printPlace(node)
            print("Incorrect type in while condition")
        return Expression()

    def visit_For(self, node):
        #check arguments of for
        type_of_array = self.visit(node.arr)
        if not isinstance(type_of_array, Array):
            self.printPlace(node)
            print("For need iterable")

        if not isinstance(node.var, AST.Variable):
            self.printPlace(node)
            print("Incorrect syntax in for")
        
        self.symbol_table = self.symbol_table.pushScope("loop")             #push new variable scope
        self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_of_array.elementTypes)) #push variable to for scope
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()                    #get old variable scope
        return Expression()
    
    def visit_If(self, node):
        type_of_cond = self.visit(node.cond)
        if not isinstance(type_of_cond, Boolean):
            self.printPlace(node)
            print("Incorrect type in if condition")

        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

        return Expression()

    def visit_Else(self, node):
        type_of_cond = self.visit(node.cond)
        if not isinstance(type_of_cond, Boolean):
            self.printPlace(node)
            print("Incorrect type in if condition")

        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.body1)
        self.symbol_table = self.symbol_table.popScope()

        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.body2)
        self.symbol_table = self.symbol_table.popScope()

        return Expression()

    def visit_Jump(self, node):
        scopes = self.symbol_table.getAllScopes()
        if not "loop" in scopes:
            self.printPlace(node)
            print("Jump expression in incorrect place: " + node.type)
        return Expression()

    def visit_Reference(self, node):
        type_of_variable = self.visit(node.variable)
        #check type of arguments
        if len(node.arguments) == 1:
            argument = node.arguments[0]
            type_of_argument = self.visit(argument)
            if not isinstance(type_of_argument, Integer):
                self.printPlace(node)
                print("Incorrect type of argument in reference")
            if not isinstance(type_of_variable, Array):
                self.printPlace(node)
                print("Incorrect reference")
        else:
            argument1 = node.arguments[0]
            type_of_argument1 = self.visit(argument1)
            argument2 = node.arguments[1]
            type_of_argument2 = self.visit(argument2)
            if not isinstance(type_of_argument1, Integer):
                self.printPlace(node)
                print("Incorrect type of argument in reference")
            if not isinstance(type_of_argument2, Integer):
                self.printPlace(node)
                print("Incorrect type of argument in reference")
            if not isinstance(type_of_variable, Matrix):
                self.printPlace(node)
                print("Incorrect reference")
        return type_of_variable.elementTypes
    
    def visit_Return(self, node):
        self.visit(node.expr)
        return Expression()

    def visit_Print(self, node):
        import Exceptions
        try:
            self.visit(node.val)
        except Exceptions.PrintException:
            self.printPlace(node)
        return Expression()

    def visit_Block(self, node):
        elements = node.body
        self.symbol_table = self.symbol_table.pushScope("body")
        for element in elements:
            self.visit(element)
        self.symbol_table = self.symbol_table.popScope()
        return Expression()

    def visit_list(self, node):
        head, *tail = node
        array_type = self.visit(head)
        for element in tail:
            type_of_element = self.visit(element)
            if not type(array_type) is type(type_of_element):
                self.wasError = True
                print("Inconsistent types in array")
                import Exceptions
                raise Exceptions.PrintException()
        return Array(array_type, len(node))


    
