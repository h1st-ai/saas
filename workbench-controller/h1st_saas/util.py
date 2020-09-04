import random
import string

_chars = list(string.ascii_lowercase) + ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
def random_char(l=10):
    return "".join([random.choice(_chars) for _ in range(l)])

def flatten_dyndb_item(item):
    v = {}

    # flatten the dict
    for k in item:
        x = list(item[k].keys())[0]
        v[k] = item[k][x]

    return v