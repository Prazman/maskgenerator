#!/usr/bin/env python
import pdb
from charMask import charMask


def main():
    pdb.set_trace()
    mask1 = charMask(maskchar="u", chartocover="")
    print mask1.gen_space
    mask2 = charMask(maskchar="", chartocover="s")
    print mask2.maskchar


if __name__ == '__main__':
    main()
