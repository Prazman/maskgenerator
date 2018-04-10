#!/usr/bin/env python
# from charMask import charMask
from stringMask import stringMask
# import sys


def main():
    print "First mask string lllldd (4 noncapitalized letters, 2 digits"
    mask1 = stringMask("lllldd", "")
    print mask1.maskstring
    print mask1.regex
    print mask1.generated_space
    words = ["abcd12", "fesc89", "ADE", "aaaa11", "zzzzaa"]
    for word in words:
        print mask1.covers(word)

    # mask2 = stringMask("", "abcd12")
    # print mask2.maskstring
    # print mask2.regex
    # print mask2.generated_space
    # print sys.version
    # mask1 = charMask("u", "")
    # print mask1
    # mask5 = charMask("H", "")
    # print mask5
    # mask2 = charMask("", "k")
    # print mask2
    # mask3 = charMask("", "2")
    # print mask3
    # mask4 = charMask("", "F")
    # print mask4


if __name__ == '__main__':
    main()
