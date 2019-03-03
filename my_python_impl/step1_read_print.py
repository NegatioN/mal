from reader import read_str
from printer import pr_str

def EVAL(x):
    return x

def READ(x):
    return read_str(x)

def PRINT(x):
    return pr_str(x)

def rep(x):
    return PRINT(EVAL(READ(x)))


while True:
    data = input('user> ')
    print(rep(data))
