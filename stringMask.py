#!/usr/bin/env python


class stringMask:
    "Mask Class"
    def __init__(self, maskstring="", stringtocover=""):
            if(maskstring != ""):
                self.maskstring = maskstring
                self.regex = self.getRegexFromString(maskstring)
            elif(stringtocover != ""):
                self.maskstring, self.regex = self.getMinimalMaskFromString()

    def getRegexFromString(maskstring):
        def getRegexFromMaskChar(char):
            if char == 'l':
                return '/l/'
            elif char == 'u':
                return '/u/'
            elif char == 'd':
                return '/d/'
            elif char == 'h':
                return '/h/'
            elif char == 'H':
                return '/H/'
            elif char == 's':
                return '/s/'
            elif char == 'a':
                return '/a/'
            elif char == 'b':
                return '/b/'
        regex = ""
        for char in maskstring:
            regex += getRegexFromMaskChar(char)
        return regex

