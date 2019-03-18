from mal_types import String

def pr_str(x):
    if isinstance(x, list):
        return "({})".format(" ".join([pr_str(y) for y in x]))
    elif isinstance(x, tuple):
        return "{}".format(" ".join([pr_str(y) for y in x]))
    elif isinstance(x, bool):
        return str(x).lower()
    elif x == None:
        return 'nil'
    elif isinstance(x, String):
        return '"{}"'.format(x)
    else:
        return str(x)