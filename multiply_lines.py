#!/usr/bin/env python

with open('test.txt','r') as fp:
	file = fp.read()
	fp.close()
	with open('test.txt','w') as fpw:
		for line in file:
			fpw.write(line + "\n" * 2)
		else:
			fpw.close()
