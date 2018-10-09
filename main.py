import sys


import ply.lex as lex
import ply.yacc as yacc

sys.path.append('./analyzers')
import lexico




if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print('You must enter a path to your file like: ./src/script.js\n')
        sys.exit()
    else:
        if(sys.argv[1] == '--help' or sys.argv[1] == '-h'):
            print('You must enter a path to your file like: ./src/script.js\n')
            sys.exit()
        else:
            f = open(sys.argv[1], "r")