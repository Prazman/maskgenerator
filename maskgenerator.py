#!/usr/bin/env python
import sys
import os
import pdb
import time
import argparse
import logging
from utils import file_len, clear_file
from stat_algorithm import stat_algorithm
from learning_algorithm import learning_algorithm

split_path = "./split/"
output_path = "./output/masks.dic"


def main():
    start_time = time.time()
    options = get_arguments()
    logging.info("Options")
    logging.info(options)
    logging_level = logging.DEBUG if options["verbose"] else logging.ERROR
    print options['verbose']
    print logging_level
    logging.getLogger().setLevel(logging_level)

    filepath = options['filepath']
    clear_file(output_path)
    print "Start mask generation for file " + filepath
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    # split files if requested, get line counts
    if options['split']:
        total_lines, rejected_lines = split_files(filepath, options["max_line_length"])
    else:
        total_lines = file_len(filepath)
        rejected_lines = file_len(split_path + "/rejected_lines")
    all_masks = []
    cumulated_generated_space = 0
    treated_lines = 0
    #only open split files of correct length
    for filename in os.listdir(split_path):
        if filename == "rejected_lines":
            continue

        if int(filename.split("file_")[1]) <= options['max_line_length']:
            with open(os.path.join(split_path, filename), 'r') as fp:
                #  lines_read, generated_space, masks = learning_algorithm(fp)
                lines_read, generated_space, masks = stat_algorithm(fp, options["max_mask_combinations"], options["mask_rejection_ratio"])
                treated_lines += lines_read
                cumulated_generated_space += generated_space
                print_status(lines_read, len(masks), cumulated_generated_space)
                print_masks_to_file(masks, lines_read, generated_space)
                all_masks += masks
                fp.close()
                logging.info("--- %s seconds ---" % (time.time() - start_time))
    else:
        total_hits = 0
        total_generated_space = 0
        for mask in all_masks:
            total_hits += mask.hitcount
            total_generated_space += mask.generated_space
        else:
            rejection_ratio = rejected_lines / float(total_lines) * 100
            coverage_ratio = total_hits / float(total_lines) * 100
            logging.info("Total Lines : " + str(total_lines))
            logging.info("Total Rejected Lines : " + str(rejected_lines))
            logging.info("Rejection Ratio : " + str(rejection_ratio))
            logging.info("\n")
            logging.info("Total treated lines : " + str(treated_lines))
            logging.info("Total hits : " + str(total_hits))
            logging.info("Coverage Ratio: {0:.2f}%".format(coverage_ratio))
        logging.info("Generated space " + str(total_generated_space))

        print "Masks Generated : " + str(len(all_masks))
        for mask in all_masks:
            print mask.maskstring
        if total_generated_space > options['max_generated_space']:
            print "Game Over"
        else:
            print "Victory"
        print_masks_to_file(all_masks, total_lines, total_generated_space)
        logging.info("--- %s seconds ---" % (time.time() - start_time))


def print_status(line_count, masks_len, total_generated_space):
    """ Prints current operation status
    """
    logging.info(str(line_count) + " words treated so far... ")
    logging.info(str(masks_len) + " masks generated so far...")
    logging.info(str(total_generated_space) + " generated space so far...")


def print_masks_to_file(masks, line_count, total_generated_space):
    """ Write generated mask list to a file
    """
    f = open(output_path, 'a')
    if len(masks) > 0:
        wordlength = len(masks[0].maskstring)
        f.write(str(line_count) + " words of length " + str(wordlength) + "\n")
        f.write('-' * 30 + "\n")
        f.write("Masklist\n")
        for mask in masks:
            f.write(mask.maskstring + "\n")
        f.write("Detailed Masklist\n")
        for mask in masks:
            relative_ratio = mask.hitcount / float(line_count) * 100
            f.write("Mask :" + mask.maskstring + "\n")
            f.write("Hits :" + str(mask.hitcount) + "\n")
            f.write("Relative Coverage ::{0:.2f}%".format(relative_ratio) + "\n")
            f.write("Regex :" + mask.regexstring + "\n")
            f.write("Generated space :" + str(mask.generated_space) + "\n\n")
        f.write("Total generated_space : " + str(total_generated_space) + "\n")
        f.write("End of masklist \n\n")
        f.write(("-" * 30 + "\n") * 3)
        f.close()


def split_files(filepath, max_line_length):
    """ Split filepath into files of same line length
        Rejects line if :
            -line is too long (max_line_length parameter)
            -line contains non ascii char and reject_special_char is true
    """
    logging.info("Start splitting operation...")
    rejection_count = 0
    total_lines = 0
    reject_file = open(split_path + "/rejected_lines", "w")
    with open(filepath) as fp:
        files = {}
        for index, line in enumerate(fp):
            if index % 10000 == 0:
                logging.info("current_line " + str(index))
                logging.info("rejection_count " + str(rejection_count))
            total_lines += 1
            line_length = len(line) - 1
            length_is_ok = line_length <= max_line_length and line_length > 1
            if length_is_ok:
                if line_length not in files:
                    name = split_path + "/file_" + str(line_length)
                    files[line_length] = open(name, 'w')
                files[line_length].write(line)
            else:
                rejection_count += 1
                reject_file.write(line)
        else:
            for f in files:
                files[f].close()
            logging.info("Total lines " + str(total_lines))
            logging.info("Rejected lines " + str(rejection_count))
            logging.info("Splitted file into same length files")
            return total_lines, rejection_count


def get_arguments():
    parser = argparse.ArgumentParser(description='Mask Generator')
    parser.add_argument('--split', dest='split', default=False, action='store_true')
    parser.add_argument("--file", dest="filepath",  required=True, type=str)
    parser.add_argument("--max_generated_space", dest="max_generated_space", default=81442800000000, type=long)
    parser.add_argument("--max_mask_combinations", dest="max_mask_combinations", default=100, type=int)
    parser.add_argument("--mask_rejection_ratio", dest="mask_rejection_ratio", default=0.03, type=float)
    parser.add_argument("--max_line_length", dest="max_line_length", default=9, type=int)
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    userOpts = vars(parser.parse_args())
    return userOpts


if __name__ == '__main__':
    main()
