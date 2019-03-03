def pr_str(x):
    if isinstance(x, list):
        return "({})".format(" ".join([pr_str(str(y)) for y in x]))
    else:
        return x