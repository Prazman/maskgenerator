from utils import do_cprofile
from charMask import charMask
from stringMask import stringMask
from collections import Counter
import itertools
import pdb
max_mask_combinations = 100
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
        return sum(mask.covers(line) for line in lines)

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
            -Generates all combinations of masks from the charsets
            -Only keep the  nth most probables combinations (max_mask_combinations)

            Example:
            First letter distribution ['u':56,'d':22,'S':1] 
            First letter distribution ['u':45]
            First letter distribution ['H':78,'d':34]

            Generated masks
            uuH
            uud
            duH
            dud
        """
        combinations = set(itertools.product(*char_stats))  # Cartesian product + set() for uniqueness
        mask_combinations = []

        for combination in combinations:
            cumulated_count = sum(count for char, count in combination)
            combination_string = "".join(char for char, count in combination)
            mask_combinations.append([cumulated_count, combination_string])
        combinations_sorted = sorted(mask_combinations, key=lambda x: x[0], reverse=True)
        kept_combinations = combinations_sorted[:max_mask_combinations]
        kept_masks = [stringMask(maskstring, "") for count, maskstring in kept_combinations]
        print "Top Generated Masks : "
        for mask in kept_masks:
            print mask.maskstring

        return kept_masks

    char_stats = []
    lines = list(file_pointer)
    line_count = len(lines)
    wordlength = len(lines[0])-1
    total_generated_space = 0
    print "Starting to treat words of length " + str(wordlength)
    print "Total lines : " + str(line_count)
    print "Max mask combinations : " + str(max_mask_combinations)
    print "Mask rejection Ratio : {0:.0f}%".format(mask_rejection_ratio * 100)
    for index in range(wordlength):   # forget \n
        print "Starting stats on letter " + str(index)
        chars_at_index = [line[index] for line in lines if line]
        charmasks_at_index = [get_char_class_from_char(item) for item in chars_at_index]
        # Generator version
        # charmasks_at_index = (get_char_class_from_char(item) for item in [line[index] for line in lines if line]) 
        char_distrib = Counter(charmasks_at_index).items()
        print "Complete Char distrib"
        print char_distrib

        char_stats.append(char_distrib)
    else:
        best_masks = build_best_masks(char_stats)
        print "Coverage calculation..."
        total_generated_space, masks = sort_best_masks(best_masks)

        return line_count, total_generated_space, masks
