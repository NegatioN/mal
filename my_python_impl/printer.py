def pr_str(x):
    if isinstance(x, list):
        return "({})".format(" ".join([pr_str(y) for y in x]))
    elif isinstance(x, bool):
        return str(x).lower()
    elif x == None:
        return 'nil'
    else:
        return str(x)