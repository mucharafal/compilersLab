#!/bin/python3
import scanner
import parser as parserFile
import sys
from TypeChecker import TypeChecker

if __name__ == '__main__':
    fh = open(sys.argv[1], "r")
    file_content = fh.read()
    parserFile.file_content = file_content
    parser = parserFile.parser
    
    ast = parser.parse(file_content, lexer=scanner.lexer)
    print(ast)
    ast.printTree()

    # Below code shows how to use visitor
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
    