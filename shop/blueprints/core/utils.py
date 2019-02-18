from re import compile

pattern = compile(r'\w+')

def slugify(string):
    return '_'.join(pattern.findall(string)).lower()


def slugify(string):
    return '_'.join(pattern.findall(string)).lower()






