from functools import reduce
import operator

from reader import read_str
from printer import pr_str
from env import Env

repl_env = Env(None)
repl_env.update({'+': lambda *x: reduce(operator.add, x),
                 '-': lambda *x: reduce(operator.sub, x),
                 '*': lambda *x: reduce(operator.mul, x),
                 '/': lambda *x: reduce(operator.truediv, x)})


def eval_ast(ast, repl_env):
    if isinstance(ast, list):
        a = [EVAL(x, repl_env) for x in ast]
        return a
    elif isinstance(ast,str): #TODO implement symbols
        try:
            return repl_env.get(ast)
        except:
            raise Exception('Couldnt locate symbol: {}'.format(ast))
    else:
        return ast



'''
symbol "let*": create a new environment using the current environment as the outer value and then use the first 
parameter as a list of new bindings in the "let*" environment. Take the second element of the binding list, 
call EVAL using the new "let*" environment as the evaluation environment, then call set on the "let*" environment 
using the first binding list element as the key and the evaluated second element as the value. This is repeated for 
each odd/even pair in the binding list. Note in particular, the bindings earlier in the list can be referred to by 
later bindings. Finally, the second parameter (third element) of the original let* form is evaluated using the 
new "let*" environment and the result is returned as the result of the let* (the new let environment is discarded upon completion).
'''
def EVAL(ast, repl_env):
    if isinstance(ast, list):
        if len(ast) > 0:
            if ast[0] == 'def!':
                repl_env.set(ast[1], EVAL(ast[2], repl_env))
            elif ast[0] == 'let*':
                e = Env(repl_env)
                e

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
