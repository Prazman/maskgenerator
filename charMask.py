#!/usr/bin/env python
import re


mask_classes = (
    ('d', '[0-9]', 10),
    ('h', '[0-9a-f]', 16),
    ('H', '[0-9A-F]', 16),
    ('l', '[a-z]', 26),
    ('u', '[A-Z]', 26),
    ('s', '[!@#\$%\^\&*\)\(+=._-]', 32),
    ('H', '[a-zA-Z0-9[!@#\$%\^\&*\)\(+=._-]', 94),
    ('d', '[\\x00-\\xFF]', 256)
)


def getCharClassFromMaskChar(maskchar, mask_classes):
    return [item for item in mask_classes if item[0] == maskchar]


def getCharClassFromChar(char, mask_classes):
    return [item for item in mask_classes if re.match(item[1], char)]


class charMask:
    def __init__(self, maskchar="", chartocover=""):
            if(maskchar != ""):
                charclass = getCharClassFromMaskChar("u", mask_classes)
                self.name,
                self.regex,
                self.generated_space = charclass[0], charclass[1], charclass[2]
            elif(chartocover != ""):
                charclass = getCharClassFromChar("Z", mask_classes)
                self.name,
                self.regex,
                self.generated_space = charclass[0], charclass[1], charclass[2]


