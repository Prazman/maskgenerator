import re
import pdb
mask_classes = (
    ('d', '[0-9]{1}', re.compile('^[0-9]{1}$'), 10),
    ('h', '[0-9a-f]{1}', re.compile('^[0-9a-f]{1}$'), 16),
    ('H', '[0-9A-F]{1}', re.compile('^[0-9A-F]{1}$'), 16),
    ('l', '[a-z]{1}', re.compile('^[a-z]{1}$'), 26),
    ('u', '[A-Z]{1}', re.compile('^[A-Z]{1}$'), 26),
    ('s', '\W|_{1}', re.compile('^\W|_{1}$'), 32),
    ('a', '[a-zA-Z0-9]\W{1}', re.compile('^[a-zA-Z0-9]\W{1}$'), 94),
    ('b', '[\\x00-\\xFF]{1}', re.compile('^[\\x00-\\xFF]{1}$'), 256)
)


class charMask:
    "Mask object for a single char --> handles mask classes"
    # Different char classes with associated info (genreated space, regex)

    _slots__ = ['name', 'regex', 'generated_space']

    # Class constructor
    def __init__(self, maskchar, chartocover):
        # Get char class from a maskchar letter (ex: luds=a)
        def getCharClassFromMaskChar(self, maskchar):
            return [item for item in mask_classes if item[0] == maskchar][0]

        # Get minimal char class matching given char
        def getCharClassFromChar(self, char):
            return [item for item in mask_classes if item[2].match(char)][0]

        if maskchar != "":
            charclass = getCharClassFromMaskChar(self, maskchar)
        elif chartocover != "":
            charclass = getCharClassFromChar(self, chartocover)
        self.name = charclass[0]
        self.regex = charclass[1]
        self.generated_space = charclass[3]
