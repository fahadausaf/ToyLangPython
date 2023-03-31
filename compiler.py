from lex import *
from parse import *
from codeGenerator import *
from tokenList import *
from helper import *
from generateExecutionTree import *
import argparse



# file_test_01 = 'input\\test_lex\\test_01_int_01.d'
# file_printf = 'input\\print.d'
# file_ifThenElse = 'input\\ifthen3.d'
# file_function = 'input\\function.d'
# file_function2 = 'input\\function2.d'
# file_function3 = 'input\\function3.d'
# file_symbolic = 'input\\symbolic2.d'
# file_assignment = 'input\\assignment.d'
# file_test = 'input\\test.d'
# file_unary = 'input\\unary.d'
# file_logical = 'input\\logicals.d'






# tokenList = lex(file_symbolic)
# # printTokens(tokenList)
# parseResult, _ = parseStatement(0, tokenList)
# code = generateStatement(parseResult)
# print()
# print(prettyPrint(code))
# print()



# print('\nSymbolic Execution\n')
# et = getExecutionTree(parseResult)
# parseExecutionTree(et)
# print()
# getConstraints(et)


# def compile(filename):
#     tokens = lex(filename)
#     ast, _ = parseStatement(0, tokens)
#     c_code = generateStatement(ast)
#     return(prettyPrint(c_code))

def cli():
    parser = argparse.ArgumentParser(
        prog='SAIL Unit Test Generator',
        description='Tooling for Automated Unit Test Generation for Sail Code'
    )

    parser.add_argument(
        '-f', '--file',
        type=str, required=True,
        help='Path of file containing SAIL code to be compiled to C'
    )

    parser.add_argument(
        '-e', '--executiontree',
        required=False, action='store_true',
        help='Generate the complete binary execution tree of the code'
    )

    parser.add_argument(
        '-c', '--constraints',
        required=False, action='store_true',
        help='Generate expressions for the constraint solver'
    )

    args = parser.parse_args()

    if(args.file):
        filename = args.file
        tokens = lex(filename)
        ast, _ = parseStatement(0, tokens)
        c_code = generateStatement(ast)
        print(prettyPrint(c_code))
        print('File: ' + str(filename) + ' compiled successfully\n')

        if(args.executiontree or args.constraints):
            execution_tree, _ = getExecutionTree(ast)
            if(args.executiontree):
                print()
                parseExecutionTree(execution_tree)

            if(args.constraints):
                print()
                getConstraints(execution_tree)

if __name__ == '__main__':
    cli()






























# print(et)
# print(et.expression)
# print(et.left)
# print(et.left.expression)
# print(et.left.left)
# print(et.left.right.expression)

# print(et.left.right.left.expression)
# print(et.left.right.left.right.expression)
# print(et.left.right.left.right.left)
# print(et.left.right.left.right.right)
# print(et.left.right.left.right.right.expression)
# print(et.left.right.left.right.right.left)
# print(et.left.right.left.right.right.right)
# print(et.left.right.left.right.right.right.expression)
# print(et.left.right.left.right.right.right.left)
# print(et.left.right.left.right.right.right.right)
# print(et.left.right.left.right.right.right.right.expression)

# print(et.left.right.left.right.right.right.right.right.expression)
# print(et.left.right.left.right.right.right.right.right.right.expression)
# print(et.left.right.left.right.right.right.right.right.right.right.expression)
# print(et.left.right.left.right.right.right.right.right.right.right.right.expression)



#print(et.left.right.right.expression)


