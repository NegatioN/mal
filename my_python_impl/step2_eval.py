from functools import reduce
import operator

from reader import read_str
from printer import pr_str

repl_env = {'+': lambda *x: reduce(operator.add, x),
            '-': lambda *x: reduce(operator.sub, x),
            '*': lambda *x: reduce(operator.mul, x),
            '/': lambda *x: reduce(operator.truediv, x)}

#TODO figure out why nested calls fail. ex: (+ 5 (* 5 3))

def eval_ast(ast, repl_env):
    if isinstance(ast, list):
        print(ast)
        a = [EVAL(x, repl_env) for x in ast]
        print(a)
        return a
    elif isinstance(ast,str): #TODO implement symbols
        return repl_env[ast]
    else:
        return ast


def EVAL(ast, repl_env):
    if isinstance(ast, list):
        if len(ast) > 0:
            evaluated = [eval_ast(x, repl_env) for x in ast]
            f = evaluated[0]
            a = f(*evaluated[1:])
            print(a)
            return a
        else:
            return ast
    else:
        return eval_ast(ast, repl_env)

def READ(x):
    return read_str(x)

def PRINT(x):
    return pr_str(x)

def rep(x):
    return PRINT(EVAL(READ(x), repl_env))


while True:
    data = input('user> ')
    print(rep(data))
