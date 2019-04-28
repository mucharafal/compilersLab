#!/usr/bin/python


class VariableSymbol():

    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol=None): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols.keys():
            return self.symbols.get(name)
        else:
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        newScope = SymbolTable(self, name)
        newScope.symbols = self.symbols.copy()
        return newScope

    def popScope(self):
        return self.parent

    def getAllScopes(self):
        if self.parent == None:
            return [self.name]
        else:
            return [self.name] + self.parent.getAllScopes()


