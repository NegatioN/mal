import re

token_exp = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)''')

class MalType:
    def __init__(self, data):
        self.data = data


class Reader:
    def __init__(self, data):
        self.arr = data
        self.cur_pos = 0

    def next(self):
        if self.cur_pos < len(self.arr):
            d = self.peek()
            self.cur_pos += 1
            return d
        else:
            return None

    def peek(self):
        return self.arr[self.cur_pos]

def read_str(x):
    return read_form(Reader(tokenize(x)))

def tokenize(x):
    return token_exp.findall(x)

def read_form(reader):
    data = reader.next()
    if data == '(':
        return read_list(reader)
    else:
        return read_atom(data)


def read_list(reader):
    data_list = []
    while True:
        try:
            data = read_form(reader)
            if data == ')':
                break
            data_list.append(data)
        except:
            raise Exception('Thats an error')

    return data_list

def read_atom(data):
    return data