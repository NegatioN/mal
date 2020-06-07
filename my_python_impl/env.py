debug = False
class Env:
    def __init__(self, outer=None, binds=None, exprs=None):
        self.data = {}
        self.outer = outer
        self.bind_exprs(binds, exprs)

    def set(self, symbol, value):
        self.data[symbol] = value

    def update(self, data):
        self.data.update(data)

    def find(self, symbol):
        try:
            return self.data[symbol]
        except Exception as e:
            if self.outer:
                return self.outer.find(symbol)
            else:
                if debug:
                    print("")
                    print('INNER:', self.data)
                    print('OUTER:', self.outer)
                raise Exception('Symbol not found', e)

    def bind_exprs(self, binds, exprs):
        binds, exprs = to_list(binds), to_list(exprs)
        if debug:
            print('BIND_EXPRS:', binds, exprs)
        if binds and exprs:
            for b, e in zip(binds, exprs):
                self.set(b, e)

    def get(self, symbol):
        return self.find(symbol)

    def __str__(self):
        return str(self.data)

def to_list(x):
    try:
        iter(x)
        return x
    except TypeError as te:
        return [x]
