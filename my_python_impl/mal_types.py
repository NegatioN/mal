class Symbol(str): pass
class Int(int): pass
class Float(float): pass
class String(str): pass
class SpecialSymbol(str): pass
class Function:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

special_symbols = ['def!', 'let*', 'if', 'do', 'fn*']


def _specialsymbol_like(s, val):
    return s == val and isinstance(s, SpecialSymbol)

def _to_symbol_type(val):
    return SpecialSymbol(val) if val in special_symbols else Symbol(val)

def func_closure(env_obj, eval_f, ast, repl_env):
    def closure(*inp):
        e = env_obj(repl_env, binds=ast[1], exprs=inp)
        return eval_f(ast[2], e)
    return Function(closure)
