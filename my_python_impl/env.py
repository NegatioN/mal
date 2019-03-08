class Env:
    def __init__(self, outer):
        self.data = {}
        self.outer = outer

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
                raise e

    def get(self, symbol):
        try:
            return self.find(symbol)
        except Exception as e:
            raise Exception('Symbol not found.', e)