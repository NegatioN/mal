import re
from mal_types import Float, Int, String, Nil, _to_symbol_type

token_exp = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)''')
int_exp = re.compile('-?\d+')
float_exp = re.compile('-?\d+\\.')

end_map = {'(': ')', '[': ']'}
list_starts = list(end_map.keys())

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
    try:
        return read_form(Reader(tokenize(x)))
    except Exception as e:
        return e #TODO propagate the whole trace

def tokenize(x):
    return token_exp.findall(x)
    #return [t for t in token_exp.findall(x) if t[0] != ';']

def read_form(reader):
    data = reader.peek()
    if data in list_starts:
        return read_list(reader)
    elif not data:
        return None
    else:
        return read_atom(reader)


def read_list(reader):
    data_list = []
    start = reader.next()
    end = end_map[start]
    while True:
        data = read_form(reader)
        if data == None:
            raise Exception("expected '{}', got EOF".format(end))
        if data == end:
            break
        data_list.append(data)
    return data_list

def read_atom(reader):
    data = reader.next()
    if float_exp.match(data):
        return Float(data)
    elif int_exp.match(data):
        return Int(data)
    elif data[0] == '"' and len(data) >= 2:
        if data[-1] == '"':
          return String(data[1:-1])
    elif data == 'nil': return Nil('nil')
    elif data == 'true': return True
    elif data == 'false': return False
    else:
        return _to_symbol_type(data)