#!/usr/bin/env python
import sys


max = 0
maxword = ""
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    word, count = line.split('\t', 1)
    # increase counters
    
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    if count > max:
        max = count
        maxword = word
    

print '%s\t%s' % (maxword, max)