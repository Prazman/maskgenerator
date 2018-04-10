#!/usr/bin/env python
import sys
import os
import pdb
import time
from stringMask import stringMask


def main():
    start_time = time.time()
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    # files = {}
    # split_files(files, filepath)
    splitpath = "./split/"
    for filename in os.listdir("./split/"):
        # name = './split/file_' + str(f)
        with open(os.path.join(splitpath, filename), 'r') as fp:
            learning_algorithm(fp)
            fp.close()
    print("--- %s seconds ---" % (time.time() - start_time))


def learning_algorithm(file_pointer):
    def createMask(masks, word, default_hitcount):
        newmask = stringMask("", word)
        newmask.hitcount = 1 if default_hitcount else 0
        masks.append(newmask)
    masks = []
    line_count = 0
    for line in file_pointer:
        line_count += 1
        if line_count % 10 == 0:
            print str(line_count) + "words so far... mask lenght " + str(len(masks))
        word = line.rstrip('\n')
        if len(masks) == 0:
            createMask(masks, word, 0)
        for mask in masks:
            # pdb.set_trace()
            if mask.covers(word):
                mask.hitcount += 1
                break
        else:
            createMask(masks, word, 1)
    else:
        f = open('masks.dic', 'a')
        if len(masks) > 0:
            wordlength = len(masks[0].maskstring)
            f.write(str(line_count) + " words of length " + str(wordlength) + "\n")
            f.write("Masklist\n")
            for mask in masks:
                f.write("Mask :" + mask.maskstring + "\n")
                f.write("Hits :" + str(mask.hitcount) + "\n")
                f.write("Ratio :" + str(mask.hitcount / float(line_count)) + "\n")
                f.write("Generated space :" + str(mask.generated_space) + "\n")
            f.write("End of masklist \n\n")
            print "End of length" + str(wordlength) + " file "
            print str(line_count) + " words treated"


def write_line_to_files(line, files):
    line_length = len(line)
    if(line_length in files):
        files[line_length].write(line)
    else:
        name = './split/file_' + str(line_length - 1)
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
