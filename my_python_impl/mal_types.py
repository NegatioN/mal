class Symbol(str): pass
class Int(int): pass
class Float(float): pass
class String(str): pass
class SpecialSymbol(str): pass

special_symbols = ['def!', 'let*']


def _specialsymbol_like(s, val):
    return s == val and isinstance(s, SpecialSymbol)

def _to_symbol_type(val):
    return SpecialSymbol(val) if val in special_symbols else Symbol(val)