import operator
from functools import reduce
from printer import pr_str
from mal_types import Nil, _cast_internal, Int, String, Atom
from reader import read_str

def prn(x):
    print(pr_str(x))
    return Nil('nil')

def equals(x, y):
    return isinstance(x, type(y)) and x == y

def swap(a, f, *args):
    #TODO? all functions are TCOFunctions, therefore we get the "normal version" that is owned by TCOFunction
    a.set(f.f(a.get(), *args))
    return a.get()

def concat(*lists):
    ml = []
    for l in lists:
        ml.extend(l)
    return ml

ns = {'+': lambda *x: _cast_internal(reduce(operator.add, x)),
      '-': lambda *x: _cast_internal(reduce(operator.sub, x)),
      '*': lambda *x: _cast_internal(reduce(operator.mul, x)),
      '/': lambda *x: _cast_internal(reduce(operator.truediv, x)),
      'prn': lambda *x: print(pr_str(x)),
      'list': lambda *x: [y for y in x],
      'str': lambda *x: String("".join(x)),
      'list?': lambda x: isinstance(x, list),
      'empty?': lambda x: len(x) == 0,
      'count': lambda x: len(x) if isinstance(x, list) else Int(0),
      '=': lambda x, y: equals(x, y),
      '>': lambda x,y: x > y,
      '>=': lambda x,y: x >= y,
      '<': lambda x,y: x < y,
      '<=': lambda x,y: x <= y,
      'read-string': read_str,
      'slurp': lambda x: String(open(x, mode='r').read()),
      'atom': lambda x: Atom(x),
      'atom?': lambda x: isinstance(x, Atom),
      'deref': lambda x: x.get(),
      'reset!': lambda a,v: a.set(v),
      'swap!': swap,
      'cons': lambda a, l: [a] + l,
      'concat': concat,
      'nth': lambda l, n: l[n],
      }

def first(l):
    if l != Nil('nil'):
        if not ns['empty?'](l):
            return l[0]
    return Nil('nil')

def rest(l):
    if l != Nil('nil'):
        if ns['count'](l) >= 2:
            return l[1:]

    return []


ns.update({'first': first,
           'rest': rest})

mal_macros = ['(def! not (fn* (a) (if a false true)))',
              '(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))',
              """(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw "odd number of forms to cond")) (cons 'cond (rest (rest xs)))))))""",
              ]
