import re
import pdb
import logging

mask_classes = (
    ('d', '[0-9]{1}', re.compile('^[0-9]{1}$'), [(48, 57)], 10),
    ('l', '[a-z]{1}', re.compile('^[a-z]{1}$'), [(97, 122)], 26),
    ('u', '[A-Z]{1}', re.compile('^[A-Z]{1}$'), [(65, 90)], 26),
    ('h', '[0-9a-f]{1}', re.compile('^[0-9a-f]{1}$'), [(48, 57), (97, 102)], 16),
    ('H', '[0-9A-F]{1}', re.compile('^[0-9A-F]{1}$'), [(48, 57), (65, 70)], 16),
    ('s', '(\W|_){1}', re.compile('^\W|_{1}$'), [(32, 47), (58, 64), (91, 96), (123, 127)], 32),
    ('a', '[a-zA-Z0-9]\W{1}', re.compile('^[a-zA-Z0-9]\W{1}$'), [(32, 127)], 94),
    ('b', '[\\x80-\\xFF]{1}', re.compile('^[\\x80-\\xFF]{1}$'), [(0, 256)], 128)
)


# Get char class from a maskchar letter (ex: luds=a)
def get_char_class_from_mask_char(maskchar):
    for mask_class in mask_classes:
        if mask_class[0] == maskchar:
            return mask_class
    else:
        logging.error('Unrecognized char mask')


def get_char_class_from_char(char):
    """ Get character class from character (Regex)
    Returns char class item
    Finds the charclass using regex
    Ex: 'a' matches regex '[a-z]{1}' --> a is class 'l'
    """
    return [item for item in mask_classes if item[2].match(char)][0]


def get_char_class_from_char_dec(char):
    """ Get character class from character (decimal)
    Returns char class item
    Finds the charclass using decimal ranges
    Ex: Decimal value of 'a' is 97 --> a is class 'l'
    """
    for mask_class in mask_classes:
        if inbounds(mask_class[3], char):
            return mask_class
    else:
        logging.error('Unrecognized character, mask b will be used instead')
        return mask_classes[-1]


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
            char_class = get_char_class_from_mask_char(maskchar)
        elif chartocover != "":
            char_class = get_char_class_from_char_dec(chartocover)
        else:
            logging.error('Could not create mask from empty char')
            char_class = mask_classes[-1]
        self.name = char_class[0]
        self.regex = char_class[1]
        self.generated_space = char_class[4]
