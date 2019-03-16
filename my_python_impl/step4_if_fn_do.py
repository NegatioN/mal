from functools import reduce
import operator
from mal_types import SpecialSymbol, Symbol, _specialsymbol_like, func_closure

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
    elif isinstance(ast, Symbol):
        return repl_env.get(ast)
    else:
        return ast

def EVAL(ast, repl_env):
    if isinstance(ast, list):
        if len(ast) > 0:
            if _specialsymbol_like(ast[0], 'def!'):
                evaled = EVAL(ast[2], repl_env)
                repl_env.set(ast[1], evaled)
                return evaled
            elif _specialsymbol_like(ast[0], 'let*'):
                e = Env(repl_env)
                counter, let_vals = 0, ast[1]
                while counter < len(let_vals) - 1:
                    val1, val2 = let_vals[counter:counter+2]
                    e.set(val1, EVAL(val2, e))
                    counter += 2

                return EVAL(ast[2], e)
            elif _specialsymbol_like(ast[0], 'do'):
                return [eval_ast(x, repl_env) for x in ast[1:]]

            elif _specialsymbol_like(ast[0], 'if'):
                e_cond = eval_ast(ast[1], repl_env)
                if e_cond is not None or e_cond is not False:
                    return eval_ast(ast[2], repl_env)
                if e_cond is False and len(ast) < 4:
                    return None
                return eval_ast(ast[3], repl_env)

            elif _specialsymbol_like(ast[0], 'fn*'):
                # what i actually WANT. is to pass in all params [a, b] etc as "binds"
                # and the following inputs ast[after_def:] as inputs? or [after_def:num_params]
                #print(ast)
                #f_param = eval_ast(ast[1], repl_env)
                #print(f_param)
                #n_env = Env(repl_env, ast[2], ast[4])
                #return EVAL(ast[4], n_env)
                return func_closure(Env, EVAL, ast, repl_env)

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
