#!/usr/bin/env python
from collections import Counter
import itertools
import pdb
from stringMask import stringMask
max_mask_combinations = 100
char_distrib = []
# test1 = ['u','u','u','u','u','u','u','u','l','l','l','l','l','d','d','d','d','d','a']
test1 = ['u','u','b','l','l']
char_distrib.append(Counter(test1).items())
# test2 = ['u','u','u','u','u','u','l','l','l','l','d','d','d','d','d']
test2 = ['u','u','l','l','l']
char_distrib.append(Counter(test2).items())
# test3 = ['u','u','u','u','u','u','u','l','l','l','l','d','d','d','d','a']
test3 = ['a','u','u','d','d']

char_distrib.append(Counter(test3).items())
# test4 = ['u','u','u','u','u','l','l','l','l','l','d','d','d']
test4 = ['d','d','d','d','d']
char_distrib.append(Counter(test4).items())

test5 = ['l','l','d','d','l']
char_distrib.append(Counter(test5).items())

test6 = ['a','l','a','d','a']
char_distrib.append(Counter(test6).items())

combinations = set(itertools.product(*char_distrib))  # Cartesian product + set() for uniqueness
mask_combinations = []

for combination in combinations:
	cumulated_count = sum(count for char,count in combination)
	combination_string = "".join(char for char,count in combination)
	mask_combinations.append([cumulated_count, combination_string])
combinations_sorted = sorted(mask_combinations, key=lambda x: x[0], reverse=True)
kept_combinations = combinations_sorted[:max_mask_combinations]
kept_masks = [stringMask(maskstring,"") for count, maskstring in kept_combinations]
print "Top Generated Masks"
for mask in kept_masks:
	print mask.maskstring
