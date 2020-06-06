class Symbol(str): pass
class Int(int): pass
class Float(float): pass
class String(str): pass
class SpecialSymbol(str): pass
class Nil(str): pass

valid_primitives = {Symbol, Int, Float, String, SpecialSymbol}


class Atom:
    def __init__(self, value):
        self.set(value)

    def __str__(self):
        return f'(atom {str(self.value)})'

    def set(self, v):
        if isinstance(v, Atom):
            self.value = v.value
        else:
            assert True in [isinstance(v, x) for x in valid_primitives], 'Atom not set to valid type.'
            self.value = v
        return self.value

    def get(self):
        return self.value


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

special_symbols = {'def!', 'let*', 'if', 'do', 'fn*', 'quote', 'quasiquote'}


def _specialsymbol_like(s, val):
    return s == val and isinstance(s, SpecialSymbol)

def _to_symbol_type(val):
    return SpecialSymbol(val) if val in special_symbols else Symbol(val)

def _is_nil(val):
    return isinstance(val, Nil)

def _cast_internal(val):
    vtype = type(val)
    if vtype == Atom:
        return _cast_internal(val.get())
    elif vtype == int:
        return Int(val)
    elif vtype == float:
         return Float(val)
    elif vtype == str:
         return String(val)
    elif val == None:
         return Nil("nil")
