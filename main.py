import sys

import lexico

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print('You must enter a path to your file like: ./src/script.js\n')
        sys.exit()
    else:
        if(sys.argv[1] == '--help' or sys.argv[1] == '-h'):
            print('You must enter a path to your file like: ./src/script.js\n')
            sys.exit()