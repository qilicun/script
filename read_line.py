#!/usr/bin/env python
import re
import numpy as np
import argparse

#parser = argparse.ArgumentParser(description="Read special keyword")
#parser.add_argument('-f', '--filen', help="Name of file", default=None, required=True)
#parser.add_argument('')
def read_to_dict(filen):
    dm = {}
    string = ""
    data = []
    with open(filen, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not len(line):
                continue
            if re.match("^-", line):
                continue
            if re.match("^/", line):
                continue
            pattern = '[a-z]'
            if re.match(pattern, line):
                string = line
                continue
            line = line.split()
            if line[-1] != "/":
                data += line
            else:
                data += line[0:-1]
                dm[string] = data
                data = []
    return dm

def get_keywords_value(dm, string):
    return dm[string]

def convert_to_ndarray(data, col):
        dm[key] = np.array(data).reshape(len(dm[key])/col,col)



#filen = "interpretation_schedule.txt"

#dm=read_to_dict(filen)
#print np.array(dm["injecting"]).reshape(len(dm["injecting"])/5,5)[:,4]
