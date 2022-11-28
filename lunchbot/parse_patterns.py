import re

def get_patterns(file: str) -> list:
    fh = open(file, "r")
    reglist = fh.readlines()

    return map(lambda s: re.compile(s), reglist)
