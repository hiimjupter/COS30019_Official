import sys

from helper.reader import *
from helper.truth_table import *
from helper.backward_chaining import *
from helper.forward_chaining import *


def main(filename, algo):
    reader = Reader(filename)

    tell_statements, query_statements = reader.read()
    print('tell_statements: ', tell_statements)
    print('query_statements: ', query_statements)

    if algo == 'TT':
        print('Truth Table')
    elif algo == 'FC':
        print('Forward Chaining')
    elif algo == 'BC':
        print('Backward Chaining')




if __name__ == "__main__":
    filename = sys.argv[1]
    algo = sys.argv[2]
    main(filename, algo)
