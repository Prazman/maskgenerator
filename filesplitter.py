#!/usr/bin/env python
import sys
import os
import pdb
import time
from collections import Counter
import cProfile
from stringMask import stringMask
from charMask import charMask


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func


def main():
    start_time = time.time()
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    # files = {}
    # split_files(files, filepath)
    splitpath = "./split/"
    for filename in os.listdir(splitpath):
        # name = './split/file_' + str(f)
        with open(os.path.join(splitpath, filename), 'r') as fp:
            # learning_algorithm(fp)
            stat_algorithm(fp)
            fp.close()
            print("--- %s seconds ---" % (time.time() - start_time))


@do_cprofile
def learning_algorithm(file_pointer):

    masks = []
    line_count = 0
    total_generated_space = 0
    for line in file_pointer:
        line_count += 1
        if line_count % 100 == 0:
            print_status(line_count, len(masks), total_generated_space)
        word = line.rstrip('\n')
        for mask in masks:
            # pdb.set_trace()
            if mask.covers(word):
                mask.hitcount += 1
                break
        else:
            newmask = stringMask("", word)
            newmask.hitcount = 0
            total_generated_space += newmask.generated_space
            masks.append(newmask)
            masks.sort(key=lambda x: x.generated_space)
    else:
        print_masks_to_file(masks, line_count)
        print "End of length" + str(masks[0].maskstring) + " file "
        print str(line_count) + " words treated"


def stat_algorithm(file_pointer):
    def get_char_class_from_char(char):
        mask = charMask("", char)
        return mask.name

    def get_coverage_count(maskstring, lines):
        counter = 0
        mask = stringMask(maskstring, "")
        for line in lines:
            if mask.covers(line):
                counter += 1
        else:
            return counter

    def get_best_mask(char_stats):
        wordlength = len(char_stats)
        bestmask = ""
        for i in range(wordlength):
            bestmaskchar = char_stats[i][0][0]
            bestmask += bestmaskchar
        else:
            return bestmask

    char_stats = []
    lines = list(file_pointer)
    wordlength = len(lines[0])
    #last char is \n
    for index in range(wordlength - 1):
        chars_at_index = [line[index] for line in lines if line]
        charmasks_at_index = map(get_char_class_from_char, chars_at_index)
        char_distrib = Counter(charmasks_at_index).items()
        char_stats.append(char_distrib)
    else:
        print char_stats
        bestmask = get_best_mask(char_stats)
        print "Best mask is " + bestmask
        cov_count = get_coverage_count(bestmask, lines)
        cov_ratio = cov_count / float(len(lines))
        print "Coverage count is" + str(cov_count)
        print "Coverage ratio is " + str(cov_ratio)


def print_status(line_count, masks_len, total_generated_space):
    print str(line_count) + " words treated so far... "
    print str(masks_len) + " masks generated"
    print str(total_generated_space) + " generated space"


def print_masks_to_file(masks, line_count):
    f = open('masks.dic', 'a')
    if len(masks) > 0:
        wordlength = len(masks[0].maskstring)
        f.write(str(line_count) + " words of length " + str(wordlength) + "\n")
        f.write("Masklist\n")
        for mask in masks:
            f.write("Mask :" + mask.maskstring + "\n")
            f.write("Hits :" + str(mask.hitcount) + "\n")
            f.write("Ratio :" + str(mask.hitcount / float(line_count)) + "\n")
            f.write("Regex :" + mask.regexstring + "\n")
            f.write("Generated space :" + str(mask.generated_space) + "\n\n")
        f.write("End of masklist \n\n")
        f.close()


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
                print "Length" + str(f) + " File was closed"
            print "Splitted file into same length files"


if __name__ == '__main__':
    main()
