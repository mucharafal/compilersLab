#!/usr/bin/python

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

    def __init__(self):
        self.symbol_table = SymbolTable(None, "main")

    def visit_BinaryExpression(self, node):
        op    = node.op
        left = node.left
        right = node.right   
        type1 = self.visit(left)
        type2 = self.visit(right)
        
        #assignment
        if op == '=':
            if isinstance(left, (AST.Variable)):
                self.symbol_table.put(left.name, VariableSymbol(left.name, type2))
                return type2
            elif isinstance(left, AST.Reference):
                if not type(type1) is type(type2):
                    print("Assignment with bad type in reference" + str(type1) + str(type2))
                
            else:
                print("Assignment to nonvariable")
        #operation and assignment
        elif op == '+=' or op == '-=' or op == '*=' or op == '/=':
            if isinstance(left, AST.Variable):
                if type(type1) == Variable:
                    print("Trying to operate on unassignment variable")
                elif type(type1) == type(type2):
                    return type1
                else:
                    print("Types in operation are wrong")
            else:
                print("Assignment to nonvariable")
        #matrix operations
        elif op == '.+' or op == '.-' or op == '.*' or op == './':
            if type(type1) is type(type2):
                return type1
            else:
                print("Incorrect types in operation " + op)
        #number operations
        elif op in ['+','-','*','/']:
            if type(type1) is type(type2):
                return type1
            else:
                print("Incorrect types in operation " + op)
        elif op in ['<', '>', '<=', '>=', '!=', '==']:
            if type(type1) is type(type2):
                return Boolean
            else:
                print("Trying to compare diffrent types")
        else:
            print("Unexprected binary expression...")
        return None

 

    def visit_Variable(self, node):
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
        print(type1)
        if node.op == 'TRANSPOSITION':
            if isinstance(type1, Matrix):
                return Matrix(type1.ySize, type1.xSize, type1.elementTypes)
            else:
                print("Transposition on bad type")
                return None
        if type(type1) is Integer or type(type1) is Float or type(type1) is Matrix:
            return type1
        print("Unary operation on bad type: " + node.op)
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
                    if type1 == self.visit(element):
                        pass
                    else:
                        print("Inconsistent types in array")
            return Array(array_type, array_size)

    def visit_Matrix(self, node):
        content = node.value
        if isinstance(content, tuple):
            #function
            functionName, size = content
            type_of_size = self.visit(size)
            if not isinstance(type_of_size, Integer):
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
                print("Type of arrays in matrix is inconsistent")
            if not head_type.size == element_type.size:
                print("Size of arrays in matrix is inconsistent")
        return Matrix(len(content), head_type.size, head_type.elementTypes)

    def visit_While(self, node):
        type_of_cond = self.visit(node.cond)
        self.symbol_table.pushScope("loop")
        self.visit(node.body)
        self.symbol_table.popScope()
        if(isinstance(type_of_cond, Boolean)):
            pass
        else:
            print("Incorrect type in while condition")
        return Expression()

    def visit_For(self, node):
        type_of_array = self.visit(node.arr)
        if isinstance(type_of_array, Array):
            pass
        else:
            print("For need iterable")
        if isinstance(node.var, AST.Variable):
            pass
        else:
            print("Incorrect syntax in for")
        #push new in SymbolTable
        self.symbol_table.pushScope("loop")
        self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_of_array))
        self.visit(node.body)
        self.symbol_table.popScope()
        return Expression()
    
    def visit_If(self, node):
        type_of_cond = self.visit(node.cond)
        self.symbol_table.pushScope("if")
        self.visit(node.body)
        self.symbol_table.popScope()
        if(isinstance(type_of_cond, Boolean)):
            pass
        else:
            print("Incorrect type in if condition")
        return Expression()

    def visit_Else(self, node):
        type_of_cond = self.visit(node.cond)
        self.symbol_table.pushScope("if")
        self.visit(node.body1)
        self.symbol_table.popScope()
        self.symbol_table.pushScope("if")
        self.visit(node.body2)
        self.symbol_table.popScope()
        if(isinstance(type_of_cond, Boolean)):
            pass
        else:
            print("Incorrect type in if condition")
        return Expression()

    def visit_Jump(self, node):
        scope = self.symbol_table.name
        if scope == "loop":
            pass
        else:
            print("Jump expression in incorrect place: " + node.type)
        return Expression()

    def visit_Reference(self, node):
        type_of_variable = self.visit(node.variable)
        #check type of arguments
        if len(node.arguments) == 1:
            argument = node.arguments[0]
            type_of_argument = self.visit(argument)
            if not isinstance(type_of_argument, Integer):
                print("Incorrect type of argument in reference")
            if not isinstance(type_of_variable, Array):
                print("Incorrect reference")
        else:
            argument1 = node.arguments[0]
            type_of_argument1 = self.visit(argument1)
            argument2 = node.arguments[1]
            type_of_argument2 = self.visit(argument2)
            if not isinstance(type_of_argument1, Integer):
                print("Incorrect type of argument in reference")
            if not isinstance(type_of_argument2, Integer):
                print("Incorrect type of argument in reference")
            if not isinstance(type_of_variable, Matrix):
                print("Incorrect reference")
        return type_of_variable.elementTypes
    
    def visit_Return(self, node):
        self.visit(node.expr)
        return Expression()

    def visit_Print(self, node):
        self.visit(node.val)
        return Expression()

    def visit_Block(self, node):
        elements = node.body
        for element in elements:
            self.visit(element)
        return Expression()

    def visit_list(self, node):
        array_size = len(node)
        head, *tail = node
        array_type = self.visit(head)
        for element in tail:
            type_of_element = self.visit(element)
            if not type(array_type) is type(type_of_element):
                print("Inconsistent types in array")
        return Array(array_type, len(node))


    
