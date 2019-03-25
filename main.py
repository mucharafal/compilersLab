import scanner
import parser
import ply.yacc as yacc
import ply.lex as lex
import sys
import AST as ast


if __name__ == '__main__':
    parser = parser.parser
    fh = open(sys.argv[1], "r")
    file_content = fh.read()
        # for p in parser.token:
        #     print(p)

    ast = parser.parse(file_content, lexer=scanner.lexer)
    ast.printTree()
