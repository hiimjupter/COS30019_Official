import sys
import os

from helper.reader import *
from helper.truth_table import *
from helper.backward_chaining import *
from helper.forward_chaining import *
from helper.convertCNF import *
from helper.resolution import *



def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'test_all':
        # Run all methods on all test files in the 'tests' directory
        test_dir = 'tests'
        test_files = sorted(
            [f for f in os.listdir(test_dir) if f.endswith('.txt')])
        algorithms = ['TT', 'FC', 'BC']
        for test_file in test_files:
            for algo in algorithms:
                print(f'\nRunning {algo} on {test_file}')
                run_algorithm(os.path.join(test_dir, test_file), algo)
    elif len(sys.argv) == 3:
        # Run the specified method on the specified test file
        filename = sys.argv[1]
        algo = sys.argv[2]
        run_algorithm(filename, algo)
    else:
        print('Usage: python iengine.py <filename> <algorithm>')
        sys.exit(1)


def run_algorithm(filename, algo):
    reader = Reader(filename)

    tell_statements, query_statement = reader.read()
    print('Tell Statements:', tell_statements)
    print('Query Statement:', query_statement)

    if algo == 'TT':
        tt = TruthTable(tell_statements, query_statement)
        result = tt.entails()
        if result:
            print('YES:', tt.entail_count)
        else:
            print('NO')
    elif algo == 'FC':
        kb_str = '; '.join(tell_statements) 
        try: 
            fc = ForwardChaining(kb_str, query_statement)
            result = fc.entails()
            if result.startswith("YES"):  # Check if the result return "YES"
                print(result) 
            else:
                print("NO")
        except ValueError as e:
            print(e) 
    elif algo == 'BC':
        kb_str = '; '.join(tell_statements)
        try: 
            bc = BackwardChaining(tell_statements)
            result = bc.backward_chain(query_statement)
            if result:
                print("YES:", ', '.join(bc.entailed_symbols))  # Print YES and the list of entailed propositions
            else: 
                print("NO")
        except ValueError as e:
            print(e) 
    elif algo == 'RS':
        # Convert tell_statements and query_statement to CNF
        tell_statements_str = '; '.join(tell_statements)  # Concatenate knowledge base
        print(f"Original Tell Statements: {tell_statements_str}")
        cnf_result = convert_to_cnf(parse_expression(tell_statements_str))
        print(f"Converted CNF: {cnf_result}")
        # Run the resolution algorithm
        result = run_resolution(cnf_result,query_statement)
        if result == True:
            print("The query is entailed by the knowledge base (Contradiction Found!).")
        else:
            print("(No Contradiction Found!)")
            
    else:
        print(f'Unknown algorithm: {algo}')


if __name__ == "__main__":
    main()
