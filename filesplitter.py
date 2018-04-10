#!/usr/bin/env python
import sys
import os
from stringMask import stringMask


def main():
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    files = {}
    split_files(files, filepath)
    for f in files:
        name = './split/file_' + str(f)
        with open(name, 'r') as fp:
            learning_algorithm(fp)
            fp.close()

def learning_algorithm(file_pointer):
    def createMask(masks, word):
        newmask = stringMask("", word)
        newmask.hitcount = 1
        masks.append(newmask)
        print "New mask " + newmask.maskstring + " for word : "+line 
    masks = []
    for line in file_pointer:
        word = line.rstrip('\n')
        if len(masks) == 0:
            createMask(masks,word)
        for mask in masks:
            if mask.covers(word):
                mask.hitcount += 1
                print "A mask already covers this string"
            else:
                print "has to create new mask because no coverage"
                createMask(masks,word)
    else:
        print "Masklist: "
        for mask in masks:
            print mask.maskstring
            print mask.hitcount


def write_line_to_files(line, files):
    line_length = len(line)
    if(line_length in files):
        files[line_length].write(line)
    else:
        name = './split/file_' + str(line_length)
        files[line_length] = open(name, 'w')
        files[line_length].write(line)


def split_files(files, filepath):
    print "Start splitting operation..."
    with open(filepath) as fp:
        for line in fp:
            write_line_to_files(line, files)
        else:
            for f in files:
                files[f].close()
                print "Length"+ str(f) + " File was closed"
            print "Splitted file into same length files"


if __name__ == '__main__':
    main()
