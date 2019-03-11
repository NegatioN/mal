from functools import reduce
import operator
from mal_types import Symbol

from reader import read_str
from printer import pr_str

repl_env = {'+': lambda *x: reduce(operator.add, x),
            '-': lambda *x: reduce(operator.sub, x),
            '*': lambda *x: reduce(operator.mul, x),
            '/': lambda *x: reduce(operator.truediv, x)}


def eval_ast(ast, repl_env):
    if isinstance(ast, list):
        a = [EVAL(x, repl_env) for x in ast]
        return a
    elif isinstance(ast, Symbol):
        try:
            return repl_env[ast]
        except:
            raise Exception('Couldnt locate symbol: {}'.format(ast))
    else:
        return ast


def EVAL(ast, repl_env):
    if isinstance(ast, list):
        if len(ast) > 0:
            args = eval_ast(ast, repl_env)
            f = args[0]
            return f(*args[1:])
        else:
            return ast
    else:
        return eval_ast(ast, repl_env)

def READ(x):
    return read_str(x)

def PRINT(x):
    return pr_str(x)

def rep(x):
    x = READ(x)
    try:
        x = EVAL(x, repl_env)
    except Exception as e:
        return e
    return PRINT(x)


while True:
    data = input('user> ')
    print(rep(data))
