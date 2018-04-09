#!/usr/bin/env python
import sys
import os


def main():
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    files = {}
    with open(filepath) as fp:
        for line in fp:
            write_line_to_files(line, files)


def write_line_to_files(line, files):
    line_length = len(line)
    if(line_length in files):
        files[line_length].write(line)
    else:
        name = './split/file_' + str(line_length)
        files[line_length] = open(name, 'w')
        files[line_length].write(line)


if __name__ == '__main__':
    main()
