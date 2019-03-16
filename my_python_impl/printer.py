from mal_types import SpecialSymbol, Function

def pr_str(x):
    if isinstance(x, list):
        return "({})".format(" ".join([pr_str(y) for y in x]))
    elif isinstance(x, Function):
        return '#<function>'
    else:
        return str(x)