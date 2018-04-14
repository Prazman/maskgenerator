#!/usr/bin/env python
# from charMask import charMask
import re
from stringMask import stringMask
from filesplitter import do_cprofile
# import sys


@do_cprofile
def main():
    # print "First mask string lllldd (4 noncapitalized letters, 2 digits"
    # mask1 = stringMask("lllldd", "")
    # print mask1.maskstring
    # print mask1.regexstring
    # # print mask1.generated_space
    # words = ["AAAZZZ!!!*=)zz12", "fesc89", "ADE", "azaa11", "zzzzaa"]
    # # for word in words:
    # #     print mask1.covers(word)
    # # with open('./split/file_10') as file_pointer:
    # #     for line in file_pointer:
    # #         word = line.rstrip('\n')
    # #         mask = maskString("",word)


    # mask2 = stringMask("", words[0])
    # print "mask 2: " + mask2.maskstring
    # for word in words:
    #     print mask2.covers(word)
    special_char_regex = re.compile("[^\x00-\x7F]")
    print special_char_regex
    a = special_char_regex.match("abcdefererer")
    b = special_char_regex.match("abcdiferùrer")
    print a, b


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
