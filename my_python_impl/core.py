import operator
from functools import reduce
from printer import pr_str
from mal_types import Nil

def prn(x):
    print(pr_str(x))
    return Nil('nil')

ns = {'+': lambda *x: reduce(operator.add, x),
      '-': lambda *x: reduce(operator.sub, x),
      '*': lambda *x: reduce(operator.mul, x),
      '/': lambda *x: reduce(operator.truediv, x),
      'prn': lambda *x: print(pr_str(x)),
      'list': lambda *x: [y for y in x],
      'list?': lambda x: isinstance(x, list),
      'empty?': lambda x: len(x) == 0,
      'count': lambda x: len(x) if isinstance(x, list) else 0,
      '=': lambda x, y: isinstance(x, type(y)) and x == y,
      '>': lambda x,y: x > y,
      '>=': lambda x,y: x >= y,
      '<': lambda x,y: x < y,
      '<=': lambda x,y: x <= y,
      }

