#!/usr/bin/env python
from charMask import charMask
import re


def getMaskRegexFromMaskString(maskstring):
    """ Builds regex concatenating regexes for one character mask
    Ex: uudl    --> ^[A-Z]{1}[A-Z]{1}[0-9]{1}[a-z]{1}$

    """
    regex = "^"
    generated_space = 1
    for char in maskstring:
        mask = charMask(char, "")
        regex += mask.regex
        generated_space = generated_space * mask.generated_space
    regex += "$"
    return regex, generated_space


def getMinimalMaskFromString(stringtocover):
    """ Build a mask matching given matchstring
        Ex: Azer123 --> 
        mask: ulllddd
        generated_space: 26*26^4*10^4
    """
    maskstring = ""
    maskregex = "^"
    generated_space = 1
    for char in stringtocover:
        mask = charMask("", char)
        maskstring += mask.name
        maskregex += mask.regex
        generated_space *= mask.generated_space
    maskregex += "$"
    return maskstring, maskregex, generated_space


class stringMask:
    "Mask object for a whole word --> handles word covering"
    _slots__ = ['maskstring', 'regex', 'generated_space', 'hitcount', 'regexstring']

    # class constructor
    def __init__(self, maskstring, stringtocover):

        self.hitcount = 0
        # Build mask from mask string (ex: lllldd)
        if maskstring != "":
            self.maskstring = maskstring
            mask = getMaskRegexFromMaskString(maskstring)
            self.regexstring = mask[0]
            self.regex = re.compile(mask[0])
            self.generated_space = mask[1]
        # Build mask from given string (ex: abcd89!)
        elif stringtocover != "":
            mask = getMinimalMaskFromString(stringtocover)
            self.maskstring = mask[0]
            self.regexstring = mask[1]
            self.regex = re.compile(mask[1])
            self.generated_space = mask[2]

    # Return True if mask covers word
    def covers(self, word):
        return self.regex.match(word) is not None
