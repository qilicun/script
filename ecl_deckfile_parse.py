#!/usr/bin/env python
import re
import numpy as np
import matplotlib.pyplot as plt
import argparse
import string

parser = argparse.ArgumentParser(description="Read special keyword")
parser.add_argument('-f', '--filen', help="Name of file", default=None, required=True)
parser.add_argument('-k', '--keyword', help="Name of keyword", default=None, required=True)
args = parser.parse_args()
filen = args.filen

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
            pattern = '[A-Z]'
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

def get_keywords_value(dm, key):
    return dm[key]

def convert_to_ndarray(dm, key, cols):
    n = len(dm[key])
    return np.array(dm[key]).reshape(n/cols, cols)

dm=read_to_dict(filen)
key = str(args.keyword)
if key == "PLYSHEAR":
    plyshear=convert_to_ndarray(dm,key, 2)
    plt.plot(plyshear[:,0], plyshear[:,1], 'r',linewidth=2)
if key == "SWOF":
    krw=convert_to_ndarray(dm,key, 4)
    plt.figure(1)
    plt.plot(krw[:,0], krw[:,1], linewidth=2, label="krw")
    plt.plot(krw[:,0], krw[:,2], linewidth=2, label="kro")
    plt.title(key)
    plt.legend()
    plt.figure(2)
    plt.plot(krw[:,0], krw[:,3], linewidth=2, label="pcwo")
    plt.title(key)
    plt.legend()
plt.show()
