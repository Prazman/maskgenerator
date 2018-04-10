#!/usr/bin/env python
from charMask import charMask


class stringMask:
    def __init__(self, maskstring, stringtocover):
        def getMaskRegexFromMaskString(maskstring):
            regex = ""
            generated_space = 1
            for char in maskstring:
                mask = charMask(char, "")
                regex += mask.regex
                generated_space = generated_space * mask.generated_space
            return regex, generated_space

        def getMinimalMaskFromString(stringtocover):
            maskstring = ""
            maskregex = ""
            generated_space = 1
            for char in stringtocover:
                mask = charMask("", char)
                maskstring += mask.name
                maskregex += mask.regex
                generated_space *= mask.generated_space
            return maskstring, maskregex, generated_space

        if(maskstring != ""):
            self.maskstring = maskstring
            mask = getMaskRegexFromMaskString(maskstring)
            self.regex = mask[0]
            self.generated_space = mask[1]
        elif(stringtocover != ""):
            mask = getMinimalMaskFromString(stringtocover)
            self.maskstring = mask[0]
            self.regex = mask[1]
            self.generated_space = mask[2]
