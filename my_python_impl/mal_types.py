class Symbol(str): pass
class Int(int): pass
class Float(float): pass
class String(str): pass
class SpecialSymbol(str): pass
class Nil(str): pass
class Function:
    def __init__(self, f):
        self.f = f
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)
    def __str__(self):
        return '#<function>'

class TCOFunction:
    def __init__(self, f, ast, env):
        self.f, self.ast, self.params, self.env = f, ast[2], ast[1], env

    def __call__(self, *args, **kwargs):
        return self.f(self.ast)

    def __str__(self):
        return '#<TCOfunction>'

special_symbols = ['def!', 'let*', 'if', 'do', 'fn*']


def _specialsymbol_like(s, val):
    return s == val and isinstance(s, SpecialSymbol)

def _to_symbol_type(val):
    return SpecialSymbol(val) if val in special_symbols else Symbol(val)

def _is_nil(val):
    return isinstance(val, Nil)

def _cast_internal(val):
    if type(val) == int:
        return Int(val)
    elif type(val) == float:
         return Float(val)
    elif type(val) == str:
         return String(val)
    elif val == None:
         return Nil("nil")
