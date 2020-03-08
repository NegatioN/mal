from mal_types import Symbol, _specialsymbol_like, Function, TCOFunction, Int

from reader import read_str
from printer import pr_str
from env import Env
from mal_types import Nil
from core import ns, mal_macros

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


import inspect
def EVAL(ast, repl_env):
    while True:
        if isinstance(ast, list):
            if len(ast) > 0:
                arg1 = ast[0]
                if _specialsymbol_like(arg1, 'do'):
                    eval_ast(ast[1:-1], repl_env)
                    ast = ast[-1]
                    continue

                elif _specialsymbol_like(arg1, 'if'):
                    o = EVAL(ast[1], repl_env)
                    # Bool truth in Python is 1, but 0 is expected.
                    if isinstance(o, Int):
                        o = not bool(o)
                    # empty types count as true values, contrary to Python
                    if o == '' or o == []:
                        o = True

                    if not isinstance(o, Nil) and o:
                        ast = ast[2]
                    else:
                        ast = ast[3] if len(ast) >= 4 else Nil('nil')
                    continue

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

                    repl_env = e
                    ast = ast[1]
                    continue

                elif _specialsymbol_like(arg1, 'fn*'):
                    def closure(*inp):
                        sub_env = Env(outer=repl_env, binds=ast[1], exprs=inp)
                        return EVAL(ast[2], sub_env)
                    return TCOFunction(Function(closure), ast, repl_env)

                r = eval_ast(ast, repl_env)
                f, args = r[0], r[1:]
                if isinstance(f, TCOFunction):
                    ast = f.ast
                    repl_env = Env(outer=f.env, binds=f.params, exprs=args)
                    continue
                else:
                    return f(*args)
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

# bootstrap macros
[rep(x) for x in mal_macros]


while True:
    data = input('user> ')
    print(rep(data))
