def EVAL(x):
    return x

def READ(x):
    return x

def PRINT(x):
    return x

def rep(x):
    return PRINT(EVAL(READ(x)))


while True:
    data = input('user> ')
    print(rep(data))
