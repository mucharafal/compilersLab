#!/usr/bin/python3

class Memory:
    #use dict as structure to store data
    #it is wrapper for dict
    def __init__(self, name): # memory name
        self.variables = {}
        self.name = name

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):         # gets from memory current value of variable <name>
        return self.variables.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value

class MemoryStack:
    #contain list of memories                                                           
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        if memory == None:
            self.stack = []
        else:
            self.stack = [memory]
        
    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in self.stack:
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        head, *tail = self.stack
        head.put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for memory in self.stack:
            if memory.has_key(name):
                memory.put(name, value)
                return
    
    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack = [memory] + self.stack
    def pop(self):          # pops the top memory from the stack
        self.stack = self.stack[1:]