#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse
import ert.ecl as ecl

parser = argparse.ArgumentParser(description="Plot WCT for comparsion")
parser.add_argument('-f', '--fn', help='Name of opm data files', default=None, required=True)
parser.add_argument('-e', '--en', help='Name of ecl data files', default=None, required=True)
parser.add_argument('-v', '--vn', nargs='+', help='Name of vectors', default=None, required=True)
##Get FPR from output/pressure/*.txt
args = parser.parse_args()
##Get FPR from output/pressure/*.txt

#load ecl result
sum_ecl = ecl.EclSum(args.en)
sum_opm = ecl.EclSum(args.fn)
#set fixed time step
scale=1e5
for v in args.vn:
    plt.figure()
    plt.title("WBHP:"+v)
    plt.plot(sum_opm.days, sum_opm.get_values("WBHP:"+v)/scale) 
    plt.plot(sum_ecl.days, sum_ecl.get_values("WBHP:"+v), color='red') 
    plt.xlabel("Time/Day")
    plt.ylabel("WBHP(bar)")
    plt.legend(["opm", "ecl"], loc='best')
    picpath="/private/miliu/data/norne/"+args.en.lower()+"_WBHP""_"+v
    plt.savefig(picpath+".png")
#plt.show()
