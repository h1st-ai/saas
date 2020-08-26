import random
import string

_chars = list(string.ascii_lowercase) + ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
def random_char(l=7):
    return "".join([random.choice(_chars) for _ in range(l)])
