#!/usr/bin/env python
import sys


max = 0
maxword = ""
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    
    word, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        continue
    
    if count > max:
        max = count
        maxword = word
    
print '%s\t%s' % (maxword, max)