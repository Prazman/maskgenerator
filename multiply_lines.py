#!/usr/bin/env python
import itertools
import pdb
char_stats = [
["a","b"],
["d","e"],
["h"],
["k"]
]
# product = char_stats[0]
# for charset in char_stats:
# 	print charset
# 	product = itertools.product(product, charset)
# print product
# for prod in product:
# 	print prod
# for char in char_stats:
# 	print char
# 	for possible_char in char:
# 		print possible_char[0]
for element in itertools.product(*char_stats):
    print(element)
# def powerset(iterable):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     s = list(iterable)
#     return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
# print list(powerset(char_stats))

# test1 = itertools.combinations(char_stats,4)
# for a in test1:
# 	print a

# test2 = itertools.permutations(char_stats,4)
# for a in test2:
# 	print a
# test = [(char_stats[0],)+x+(char_stats[-1],) for i in range(len(char_stats)-1) for x in combinations(char_stats[1:-1],i)]
# with open('test.txt','r') as fp:
# 	file = fp.read()
# 	fp.close()
# 	with open('test.txt','w') as fpw:
# 		for line in file:
# 			fpw.write(line + "\n" * 2)
# 		else:
# 			fpw.close()
