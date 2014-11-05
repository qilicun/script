#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import ert.ecl as ecl

import argparse
parser = argparse.ArgumentParser(description="Plot WCT for comparsion")
parser.add_argument('-f', '--fn', help='Name of opm data files', default=None, required=True)
parser.add_argument('-e', '--en', help='Name of ecl data files', default=None, required=True)
parser.add_argument('-v', '--vn', nargs='+', help='Name of wells', default=None, required=True)

args = parser.parse_args()

sum_ecl = ecl.EclSum(args.en)
sum_opm = ecl.EclSum(args.fn)

for v in args.vn:
    plt.figure()
    plt.title(v)
    plt.plot(sum_opm.days, sum_opm.get_values("WWPR:"+v)/(sum_opm.get_values("WWPR:"+v)+sum_opm.get_values("WOPR:"+v))) 
    plt.plot(sum_ecl.days, sum_ecl.get_values("WWCT:"+v), color='red') 
    plt.xlabel("Time(Day)")
    plt.ylabel("Water cut")
    plt.legend(["opm", "ecl"], loc='best')
    picpath="/private/miliu/data/norne/"+args.en.lower()+"_WWCT_"+v
    plt.savefig(picpath+".png")

