from mal_types import Symbol, _to_symbol_type, _specialsymbol_like, Function, Int

from reader import read_str
from printer import pr_str
from env import Env
from mal_types import Nil
from core import ns, mal_macros

repl_env = Env(None)
repl_env.update(ns)
repl_env.update({'eval': lambda ast: EVAL(ast, repl_env)})

def eval_ast(ast, repl_env):
    if isinstance(ast, list):
        a = [EVAL(x, repl_env) for x in ast]
        return a
    elif isinstance(ast, Symbol):
        return repl_env.get(ast)
    else:
        return ast

def is_pair(ast):
    if not isinstance(ast, list):
        return False
    return len(ast) > 0


def quasiquote(ast):
    if not is_pair(ast):
        return [_to_symbol_type('quote'), ast]
    elif ast[0] == 'unquote':
        return ast[1]

    if is_pair(ast[0]):
        if ast[0][0] == 'splice-unquote':
            p1, p2 = ast[0][1], quasiquote(ast[1:])
            return [_to_symbol_type('concat'), p1, p2]
    return [_to_symbol_type('cons'), quasiquote(ast[0]), quasiquote(ast[1:])]

def is_macro_call(ast, env):
    try:
        data = env.get(ast[0]) # exists in env
        return data.is_macro
    except:
        return False

def macroexpand(ast, env):
    while is_macro_call(ast, env):
        macro_f = env.get(ast[0])
        args = ast[1:]
        ast = macro_f(args)
    return ast

def EVAL(ast, repl_env):
    while True:

        if not isinstance(ast, list):
            return eval_ast(ast, repl_env)

        ast = macroexpand(ast, repl_env)

        if not isinstance(ast, list):  # Macro-expansion can return singleton.
            return eval_ast(ast, repl_env)

        if len(ast) == 0:
            return ast

        arg1 = ast[0]
        if _specialsymbol_like(arg1, 'def!'):
            evaled = EVAL(ast[2], repl_env)
            repl_env.set(ast[1], evaled)
            return evaled

        elif _specialsymbol_like(arg1, 'defmacro!'):
            evaled = EVAL(ast[2], repl_env)
            evaled.is_macro = True
            repl_env.set(ast[1], evaled)
            return evaled

        elif _specialsymbol_like(arg1, 'macroexpand'):
            return macroexpand(ast[1], repl_env)

        elif _specialsymbol_like(arg1, 'let*'):
            e = Env(repl_env)
            counter, let_vals = 0, ast[1]
            while counter < len(let_vals) - 1:
                val1, val2 = let_vals[counter:counter+2]
                e.set(val1, EVAL(val2, e))
                counter += 2

            repl_env = e
            ast = ast[1]

        elif _specialsymbol_like(arg1, 'quote'):
            return ast[1]

        elif _specialsymbol_like(arg1, 'quasiquote'):
            ast = quasiquote(ast[1])

        elif _specialsymbol_like(arg1, 'do'):
            eval_ast(ast[1:-1], repl_env)
            ast = ast[-1]

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

        elif _specialsymbol_like(arg1, 'fn*'):
            return Function(EVAL, Env, ast[2], repl_env, ast[1])

        else:
            # we always hit a function here?

            r = eval_ast(ast, repl_env)
            f, args = r[0], r[1:]
            if isinstance(f, Function):
                ast = f.ast
                repl_env = f.gen_env(args)
            else:
                return f(*args)

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
