#!/usr/bin/env python
import sys
import os
import pdb
import time
import itertools
from collections import Counter
import cProfile
from stringMask import stringMask
from charMask import charMask
maximum_generated_space = 81442800000000
char_rejection_ratio = 0.05
mask_rejection_ratio = 0.03
splitpath = "./split/"

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
    split = kwargs.get('split',False)
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    split_files()
    all_masks = []
    total_generated_space = 0
    total_lines = 0
    for filename in os.listdir(splitpath):
        # name = './split/file_' + str(f)
        with open(os.path.join(splitpath, filename), 'r') as fp:
            #  lines_read, generated_space, masks = learning_algorithm(fp)
            lines_read, generated_space, masks = stat_algorithm(fp)
            all_masks += masks
            total_generated_space += generated_space
            total_lines += lines_read
            fp.close()
            print("--- %s seconds ---" % (time.time() - start_time))
    else:
        total_hitratio = 0
        for mask in all_masks:
            total_hitratio += mask.hitcount
        else:
            print "Total hits " + str(total_hitratio)
            print "Total Lines" + str(total_lines)
            print "Coverage Ratio: {percent:.2%}%".format( total_hitratio / float(total_lines))
        print "Generated space " + str(total_generated_space)
        if total_generated_space > maximum_generated_space:
            print "Game Over"
        else:
            print "Victory"


@do_cprofile
def learning_algorithm(file_pointer):
    """ Get exhaustive mask list from learning
        -Take the first word, build a minimal mask
        -Try the mask against the second word
            -If matches, continue
            -Else build a second mask
        -Try the 2 first masks against the 3rd word
        -So on...
    """
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
        print "End of length " + str(masks[0].maskstring) + " file "
        print str(line_count) + " words treated"
        return line_count, total_generated_space, masks


@do_cprofile
def stat_algorithm(file_pointer):
    """ Build a list of masks from character distribution 
    """
    def get_char_class_from_char(char):
        mask = charMask("", char)
        return mask.name

    def get_coverage_count(mask):
        """ Count lines matching mask
        """
        return len([line for line in lines if mask.covers(line)])

    def sort_best_masks(masks):
        """ Get best masks from coverage calculation
        Returns a list of masks
        -Calculate coverage for each mask (ratio is relative to file length)
        - Rejects weakest masks (mask_rejection_ratio)
        """
        total_generated_space = 0
        kept_masks = []
        print "Generated masks " + str(len(masks))
        for mask in masks:
            mask.hitcount = get_coverage_count(mask)
            hitratio = mask.hitcount / float(line_count)
            if hitratio > mask_rejection_ratio:
                kept_masks.append(mask)
                total_generated_space += mask.generated_space
                print mask.maskstring + " Kept with ratio : {percent:.2%}%".format(hitratio)
            else:
                print mask.maskstring + " Rejected with ratio : {percent:.2%}%".format(hitratio)
        else:
            print "Kept masks " + str(len(masks))
            return total_generated_space, kept_masks

    def build_best_masks(char_stats):
        """ Build best masks from char distribution
            Returns a list of masks
            -Removes rarest charclasses from charsets
            -Generates all combinations of masks from the charsets

            Example:
            First letter distribution ['u':56,'d':22,'S':1] --> should reject S
            First letter distribution ['u':45]
            First letter distribution ['H':78,'d':34]

            Generated masks
            uuH
            uud
            duH
            dud
        """
        masks = []
        charsets_matrix = []
        total = float(line_count)
        for stats in char_stats:
            charset = [char for char, count in stats.items() if count / total > char_rejection_ratio] #only keep class with frequency > char_rejection_ratio
            charsets_matrix.append(charset)
        combinations = set(itertools.product(*charsets_matrix))  # Cartesian product + set() for uniqueness
        for element in combinations:
            maskstring = "".join(element)
            masks.append(stringMask(maskstring, ""))

        return masks

    char_stats = []
    lines = list(file_pointer)
    line_count = len(lines)
    wordlength = len(lines[0])
    total_generated_space = 0
    print "Starting to treat words of length " + str(wordlength)
    print "Total lines : " + str(line_count)
    print "Char Rejection Ratio : {0:.0f}%".format(char_rejection_ratio * 100)
    print "Mask rejection Ratio : {0:.0f}%".format(mask_rejection_ratio * 100)
    for index in range(wordlength - 1): #forget \n
        print "Starting stats on letter " + str(index)
        chars_at_index = [line[index] for line in lines if line]
        charmasks_at_index = [get_char_class_from_char(item) for item in chars_at_index]
        # Generator version
        # charmasks_at_index = (get_char_class_from_char(item) for item in [line[index] for line in lines if line]) 
        char_distrib = Counter(charmasks_at_index)
        print "Complete Char distrib"
        print char_distrib

        char_stats.append(char_distrib)
    else:
        best_masks = build_best_masks(char_stats)
        print "Coverage calculation..."
        total_generated_space, masks = sort_best_masks(best_masks)
        print_status(line_count, len(masks), total_generated_space)
        print_masks_to_file(masks, len(lines),total_generated_space)
        return line_count, total_generated_space, masks


def print_status(line_count, masks_len, total_generated_space):
    print str(line_count) + " words treated so far... "
    print str(masks_len) + " masks generated"
    print str(total_generated_space) + " generated space"


def print_masks_to_file(masks, line_count,total_generated_space):
    f = open('masks.dic', 'w')
    if len(masks) > 0:
        wordlength = len(masks[0].maskstring)
        f.write(str(line_count) + " words of length " + str(wordlength) + "\n")
        f.write("Masklist\n")
        for mask in masks:
            f.write("Mask :" + mask.maskstring + "\n")
            f.write("Hits :" + str(mask.hitcount) + "\n")
            f.write("Ratio ::{0:.0f}%".format(mask.hitcount / float(line_count) * 100) + "\n")
            f.write("Regex :" + mask.regexstring + "\n")
            f.write("Generated space :" + str(mask.generated_space) + "\n\n")
        f.write("Total generated_space : " + str(total_generated_space))
        f.write("End of masklist \n\n")
        f.write(("-" * 30 + "\n")*3)
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
    shuffle = True
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
