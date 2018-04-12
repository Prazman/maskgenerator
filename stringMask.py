#!/usr/bin/env python
from charMask import charMask
import re


class stringMask:
    "Mask object for a whole word --> handles word covering"
    _slots__ = ['maskstring', 'regex', 'generated_space', 'hitcount', 'regexstring']

    # class constructor
    def __init__(self, maskstring, stringtocover):
        # get the regex and generated space corresponding to mask string (ex: llldd)
        def getMaskRegexFromMaskString(maskstring):
            regex = "^"
            generated_space = 1
            for char in maskstring:
                mask = charMask(char, "")
                regex += mask.regex
                generated_space = generated_space * mask.generated_space
            regex += "$"
            return regex, generated_space

        # get the name, regex and generated space for the minimal mask generated from a string
        def getMinimalMaskFromString(stringtocover):
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
