from utils import do_cprofile
from charMask import charMask
from stringMask import stringMask
from collections import Counter
import itertools
char_rejection_ratio = 0.10
mask_rejection_ratio = 0.03


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
        kept_masks = []
        total_generated_space = 0
        print "Generated masks " + str(len(masks))
        for mask in masks:
            mask.hitcount = get_coverage_count(mask)
            hitratio = mask.hitcount / float(line_count)
            if hitratio > mask_rejection_ratio:
                kept_masks.append(mask)
                total_generated_space += mask.generated_space
                print mask.maskstring + " Kept with ratio : {0:.2f}%".format(hitratio * 100)
            else:
                print mask.maskstring + " Rejected with ratio : {0:.2f}%".format(hitratio * 100)
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
    for index in range(wordlength - 1):   # forget \n
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

        return line_count, total_generated_space, masks
