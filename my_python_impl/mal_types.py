class Symbol(str): pass
class Int(int): pass
class Float(float): pass
class String(str): pass
class SpecialSymbol(str): pass
class Nil(str): pass

valid_primitives = {Symbol, Int, Float, String, SpecialSymbol}

debug = False

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
    def __init__(self, Eval, Env, ast, env, params):
        self.Eval, self.Env, self.ast, self.env, self.params = Eval, Env, ast, env, params
        self.is_macro = False

    def gen_env(self, args):
        return self.Env(outer=self.env, binds=self.params, exprs=args)

    def __call__(self, *inp):
        sub_env = self.gen_env(*inp)
        if debug:
            print('INP:', *inp)
            print('PARAMS:', self.params)
            print('SUB_ENV:', sub_env)
        return self.Eval(self.ast, sub_env)

special_symbols = {'def!', 'defmacro!', 'let*', 'if', 'do', 'fn*', 'quote', 'quasiquote', 'macroexpand'}


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
