import re

token_exp = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)''')
int_exp = re.compile('\d+')
float_exp = re.compile('\d+\\.')

end_map = {'(': ')', '[': ']'}

class MalType:
    def __init__(self, data):
        self.data = data


class Reader:
    def __init__(self, data):
        self.arr = data
        self.cur_pos = 0

    def next(self):
        self.cur_pos += 1
        return self.arr[self.cur_pos - 1]

    def peek(self):
        if self.cur_pos < len(self.arr):
            return self.arr[self.cur_pos]
        else:
            return None

def read_str(x):
    return read_form(Reader(tokenize(x)))

def tokenize(x):
    return token_exp.findall(x)

def read_form(reader):
    data = reader.peek()
    if data in ['(']:
        return read_list(reader)
    elif not data:
        return None
    else:
        return read_atom(reader)


def read_list(reader):
    data_list = []
    start = reader.next()
    print(start)
    end = end_map[start]
    while True:
        data = read_form(reader)
        if not data:
            raise Exception("expected '{}', got EOF".format(end))
        if data == end:
            break
        data_list.append(data)

    return data_list

def read_atom(reader):
    data = reader.next()
    if float_exp.match(data):
        return float(data)
    elif int_exp.match(data):
        return int(data)
    else:
        return data