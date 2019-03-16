from mal_types import SpecialSymbol, Symbol, _specialsymbol_like, Function, \
    Nil, Int

from reader import read_str
from printer import pr_str
from env import Env
from core import ns

repl_env = Env()
repl_env.update(ns)


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
                e_cond = EVAL(ast[1], repl_env)

                # Bool truth in Python is 1, but 0 is expected.
                # Special casing. TODO move
                if isinstance(e_cond, Int):
                    e_cond = not bool(e_cond)
                if not isinstance(e_cond, Nil) and e_cond != False:
                    return EVAL(ast[2], repl_env)
                else:
                    if len(ast) >= 4:
                        return EVAL(ast[3], repl_env)
                    return Nil('nil')

            elif _specialsymbol_like(ast[0], 'fn*'):
                def closure(*inp):
                    return EVAL(ast[2],
                                Env(repl_env,
                                    binds=ast[1],
                                    exprs=inp))
                return Function(closure)

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
