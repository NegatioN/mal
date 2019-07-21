import operator
from functools import reduce
from printer import pr_str
from mal_types import Nil, _cast_internal

def prn(x):
    print(pr_str(x))
    return Nil('nil')

def equals(x, y):
    return isinstance(x, type(y)) and x == y

ns = {'+': lambda *x: _cast_internal(reduce(operator.add, x)),
      '-': lambda *x: _cast_internal(reduce(operator.sub, x)),
      '*': lambda *x: _cast_internal(reduce(operator.mul, x)),
      '/': lambda *x: _cast_internal(reduce(operator.truediv, x)),
      'prn': lambda *x: print(pr_str(x)),
      'list': lambda *x: [y for y in x],
      'list?': lambda x: isinstance(x, list),
      'empty?': lambda x: len(x) == 0,
      'count': lambda x: len(x) if isinstance(x, list) else Int(0),
      '=': lambda x, y: equals(x, y),
      '>': lambda x,y: x > y,
      '>=': lambda x,y: x >= y,
      '<': lambda x,y: x < y,
      '<=': lambda x,y: x <= y,
      }

