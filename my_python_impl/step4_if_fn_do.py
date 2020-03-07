from mal_types import String, Symbol, _specialsymbol_like, Function, Int

from reader import read_str
from printer import pr_str
from env import Env
from mal_types import Nil
from core import ns

repl_env = Env(None)
repl_env.update(ns)


def eval_ast(ast, repl_env):
    if isinstance(ast, list):
        a = [EVAL(x, repl_env) for x in ast]
        return a
    elif isinstance(ast, Symbol):
        try:
            return repl_env.get(ast)
        except:
            raise Exception('Couldnt locate symbol: {}'.format(ast))
    else:
        return ast



def EVAL(ast, repl_env):
    if isinstance(ast, list):
        if len(ast) > 0:
            arg1 = ast[0]
            if _specialsymbol_like(arg1, 'do'):
                return eval_ast(ast[1:], repl_env)[-1]

            elif _specialsymbol_like(arg1, 'if'):
                o = EVAL(ast[1], repl_env)
                # Bool truth in Python is 1, but 0 is expected.
                if isinstance(o, Int):
                    o = not bool(o)
                # empty types count as true values, contrary to Python
                if o == '' or o == []:
                    o = True


                if not isinstance(o, Nil) and o:
                    return EVAL(ast[2], repl_env)
                return EVAL(ast[3], repl_env) if len(ast) >= 4 else Nil

            elif _specialsymbol_like(arg1, 'def!'):
                evaled = EVAL(ast[2], repl_env)
                repl_env.set(ast[1], evaled)
                return evaled

            elif _specialsymbol_like(arg1, 'let*'):
                e = Env(repl_env)
                counter, let_vals = 0, ast[1]
                while counter < len(let_vals) - 1:
                    val1, val2 = let_vals[counter:counter+2]
                    e.set(val1, EVAL(val2, e))
                    counter += 2

                return EVAL(ast[2], e)

            elif _specialsymbol_like(arg1, 'fn*'):
                def closure(*inp):
                    sub_env = Env(outer=repl_env, binds=ast[1], exprs=inp)
                    return EVAL(ast[2], sub_env)
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
