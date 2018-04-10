#!/usr/bin/env python
from charMask import charMask
import sys


def main():
    print sys.version
    mask1 = charMask("u", "")
    print mask1
    mask5 = charMask("H", "")
    print mask5
    mask2 = charMask("", "k")
    print mask2
    mask3 = charMask("", "2")
    print mask3
    mask4 = charMask("", "F")
    print mask4


if __name__ == '__main__':
    main()
