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
        cnt = 0
        for line in fp:
            write_line_to_files(line,files)


def write_line_to_files(line,files):
    l = len(line)
    if(l in files):
        files[l].write(line)
    else:
        name = './split/file_'+str(l)
        files[l]=open(name,'w')
        files[l].write(line)
#  sorted_lengths = order_line_length_array(line_length_array, desc=True)
#   print("Length {}".format(sorted_lengths))

# def order_line_length_array(line_length_array, desc=False):  
#    lengths = [(length, cnt) for length, cnt in line_length_array.items()]
#    return sorted(lengths, key=lambda x: x[1], reverse=desc)

# def record_line_length(line, line_length_array):  
#   l = len(line)
#   if l in line_length_array:
#     line_length_array[l]+=1
#   else:
#     line_length_array[l]=1

if __name__ == '__main__':  
   main()