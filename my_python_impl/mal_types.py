class Symbol(str): pass
class Int(int): pass
class Float(float): pass
class String(str): pass

def _symbol_like(s, val):
    return s == val and isinstance(s, Symbol)