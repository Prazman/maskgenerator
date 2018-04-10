import re


class charMask:
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

    def __init__(self, maskchar, chartocover):

        def getCharClassFromMaskChar(self, maskchar):
            return [item for item in self.mask_classes if item[0] == maskchar][0]

        def getCharClassFromChar(self, char):
            return [item for item in self.mask_classes if re.match(item[1], char)][0]

        if(maskchar != ""):
                charclass = getCharClassFromMaskChar(self, maskchar)
                print charclass
                self.name = charclass[0]
                self.regex = charclass[1]
                self.generated_space = charclass[2]
        elif(chartocover != ""):
                charclass = getCharClassFromChar(self, chartocover)
                print charclass
                self.name = charclass[0]
                self.regex = charclass[1]
                self.generated_space = charclass[2]
