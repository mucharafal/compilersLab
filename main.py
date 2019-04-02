#!/bin/python3
import scanner
import parser
import sys

if __name__ == '__main__':
    parser = parser.parser
    fh = open(sys.argv[1], "r")
    file_content = fh.read()
        # for p in parser.token:
        #     print(p)

    ast = parser.parse(file_content, lexer=scanner.lexer)
    ast.printTree()
