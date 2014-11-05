#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import ert.ecl as ecl

import argparse
parser = argparse.ArgumentParser(description="Plot WCT for comparsion")
parser.add_argument('-f', '--fn', help='Name of opm data files', default=None, required=True)
parser.add_argument('-e', '--en', help='Name of ecl data files', default=None, required=True)
parser.add_argument('-v', '--vn', nargs='+', help='Name of vectors', default=None, required=True)

args = parser.parse_args()

sum_ecl = ecl.EclSum(args.en)
sum_opm = ecl.EclSum(args.fn)

print sum_ecl, sum_opm
#load ecl result
#ecl=[]
#opm=[]
#ecl.append(sum_ecl.days)
#ecl.append(sum_opm.days)
#for v in args.vn:
#    ecl.append(sum_ecl.get_values(args.vn))
#    ecl.append(sum_opm.get_values(args.vn))

scale = 2000/2.67918e-07
print scale
for v in args.vn:
    plt.figure()
    plt.title(v)
    plt.plot(sum_opm.days, sum_opm.get_values(v)*scale) 
    print sum_opm.get_values(v)*scale
    plt.plot(sum_ecl.days, sum_ecl.get_values(v), color='red') 
    plt.xlabel("Time(Day)")
    plt.ylabel("Rate(m^3/day)")
    plt.legend(["opm", "ecl"], loc='best')
    picpath="/private/miliu/data/norne/"+args.en.lower()+"_"+v.split(':')[0]+"_"+v.split(":")[1]
    plt.savefig(picpath+".png")
#plt.show()
