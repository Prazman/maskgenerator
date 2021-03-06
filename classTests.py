#!/usr/bin/env python
# from charMask import charMask
import re
from stringMask import stringMask
from filesplitter import do_cprofile



@do_cprofile
def main():
    """ This script is only a playground to test charMask and StringMask classes
    """
    # print "First mask string lllldd (4 noncapitalized letters, 2 digits"
    # mask1 = stringMask("lllldd", "")
    # print mask1.maskstring
    # print mask1.regexstring
    # print mask1.generated_space
    # words = ["AAAZZZ!!!*=)zz12", "fesc89", "ADE", "azaa11", "zzzzaa"]
    # for word in words:
    #     print mask1.covers(word)



    # mask2 = stringMask("", words[0])
    # print "mask 2: " + mask2.maskstring
    # for word in words:
    #     print mask2.covers(word)


    # mask2 = stringMask("", "abcd12")
    # print mask2.maskstring
    # print mask2.regex
    # print mask2.generated_space
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
    masklist = ["ss","su","uu","ll","sl"]
    masks = [stringMask(mask,"") for mask in masklist]
    with open('./split/file_2') as fp:
        for line in fp:
            word= line.rstrip('\n')
            for mask in masks:
                print mask.maskstring + " covers " + word +" : " + str(mask.covers(word))
                print mask.regexstring
    fp.close()


if __name__ == '__main__':
    main()
