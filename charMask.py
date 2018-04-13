import re
import pdb

mask_classes = (
    ('d', '[0-9]{1}', re.compile('^[0-9]{1}$'), [(48, 57)], 10),
    ('l', '[a-z]{1}', re.compile('^[a-z]{1}$'), [(97, 122)], 26),
    ('u', '[A-Z]{1}', re.compile('^[A-Z]{1}$'), [(65, 90)], 26),
    ('h', '[0-9a-f]{1}', re.compile('^[0-9a-f]{1}$'), [(48, 57), (97, 102)], 16),
    ('H', '[0-9A-F]{1}', re.compile('^[0-9A-F]{1}$'), [(48, 57), (65, 70)], 16),
    ('s', '\W|_{1}', re.compile('^\W|_{1}$'), [(32, 47), (58, 64), (87, 91), (123, 127)], 32),
    ('a', '[a-zA-Z0-9]\W{1}', re.compile('^[a-zA-Z0-9]\W{1}$'), [(32, 127)], 94),
    ('b', '[\\x00-\\xFF]{1}', re.compile('^[\\x00-\\xFF]{1}$'), [(32, 256)], 256)
)


# Get char class from a maskchar letter (ex: luds=a)
def getCharClassFromMaskChar(maskchar):
    return [item for item in mask_classes if item[0] == maskchar][0]


def getCharClassFromChar(char):
    """ Get character class from character (Regex)
    Returns char class item
    Finds the charclass using regex
    Ex: 'a' matches regex '[a-z]{1}' --> a is class 'l'
    """
    return [item for item in mask_classes if item[2].match(char)][0]


def getCharClassFromCharDec(char):
    """ Get character class from character (decimal)
    Returns char class item
    Finds the charclass using decimal ranges
    Ex: Decimal value of 'a' is 97 --> a is class 'l'
    """
    return [item for item in mask_classes if inbounds(item[3], char)][0]


def inbounds(boundaries_array, char):
    """ Is value between set of bounds
    Ex: Boundset = [(1, 8), (25, 32)]
    7 is in bounds
    15 is out bounds
    28 is in bounds
    """
    dec_value = ord(char)
    for bounds in boundaries_array:
        if dec_value <= bounds[1] and dec_value >= bounds[0]:
            return True
    else:
        return False


class charMask:
    "Mask object for a single char --> charclass character to charclass, or char to charclass"
    # Different char classes with associated info (genreated space, regex)

    _slots__ = ['name', 'regex', 'generated_space']

    # Class constructor
    def __init__(self, maskchar, chartocover):

        if maskchar != "":
            charclass = getCharClassFromMaskChar(maskchar)
        elif chartocover != "":
            charclass = getCharClassFromCharDec(chartocover)
        self.name = charclass[0]
        self.regex = charclass[1]
        self.generated_space = charclass[4]
