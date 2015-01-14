#!/usr/bin/env python
# The MIT License (MIT)
# 
# Copyright (c) 2015 Albert Lee
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This script progressively produces the commands that will merges the fasta file(s) specified in the given list.
# Once you get the list of commands. you can run them locally or using cluster
# 
# progressive_merge_cd_hit.py <LIST_OF_FASTA_FILES>

from sys import argv
from random import shuffle
from itertools import izip_longest
import re
import os

threshold = 0.99
#prefix = "merge"

def print_cd_hit_cmd(f1,f2):

    output = os.path.basename(simplify_name(f1)) + "_" + os.path.basename(simplify_name(f2)) + ".fa"
    print "cd-hit-est -i <(cat %s %s) -o %s -M 0 -c %.2f" % (f1, f2, output,threshold)
    return output
def simplify_name(a):
    return re.sub(r"_\w_\w\w_","",a).replace("infoAdded.fasta","").replace(".fa","")

def recursive_merge(given_list):
    if len(given_list) == 1:
	return

    slice1 = given_list[::2]  # even list
    slice2 = given_list[1::2] # odd list
    merged = list(izip_longest(slice1, slice2))

    output_list = []
    # run cd-hit for each item in thet list
    for (a,b) in merged :
	if( a == None or b == None):
	    # when there is one item
	    # just pass
	    if( a == None ):
		output = b
	    else:
		output = a
	else:
	    # do merge
	    output = print_cd_hit_cmd(a,b)
	output_list.append(output)
    return(recursive_merge(output_list))

# get the list of objects
script, fname = argv

with open(fname) as f:
    content = f.read().splitlines() 

#shuffle(content)
recursive_merge(content)
