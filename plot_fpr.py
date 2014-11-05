#!/bin/env python

import numpy as np
import glob
import matplotlib.pyplot as plt
import os
import ert.ecl as ecl

import argparse
parser = argparse.ArgumentParser(description="Plot FPR for comparsion")
parser.add_argument('-f', '--fn', help='Name of opm data files', default=None, required=True)
parser.add_argument('-e', '--en', help='Name of ecl data files', default=None, required=True)
parser.add_argument('-p', '--pn', help='Name of pv data files', default=None, required=True)
##Get FPR from output/pressure/*.txt
args = parser.parse_args()

timestep=[0]+[1,2,3,4,5,5,10,10]+[20]*3+[25]*8#+[50]*34#+[100]*80

def get_opm_pav(path, pvpath):
    pfiles = glob.glob(path+'/pressure/*.txt')
    pfiles.sort()
    sfiles = glob.glob(path+'/saturation/*.txt')
    sfiles.sort()
    tmp=[]
    pv = np.loadtxt(pvpath)
    for i in range(0, len(timestep)):
        sum1=0
        sum2=0
        p = np.loadtxt(pfiles[i])
        sw = np.loadtxt(sfiles[i])
        print len(p), len(sw), len(pv)
        for cell in range(0, len(p)):
           sum1 += p[cell]*pv[cell]*(1-sw[3*cell])
           sum2 += pv[cell]*(1-sw[3*cell])
        tmp.append(sum1/sum2)
    return np.array(tmp)
print "Starting plot field pressure\n"
opm_pav = get_opm_pav(args.fn, args.pn)
#load ecl result
ecl_pav = ecl.EclSum(args.en)
#set fixed time step
#timestep =[0,1.0, 1.0, 1.0, 1.5, 1.5, 4.0, 5.0, 5.0, 5.0, 5.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2.0, 2.5, 3.9099999999999966, 5.7900000000000063, 5.7999999999999972, 12.5, 12.5, 12.5, 12.5, 25.0, 2.5, 3.1200000000000045, 4.8899999999999864, 7.2400000000000091, 7.25, 12.5, 12.5, 25.0, 2.5, 3.1200000000000045, 4.8899999999999864, 7.2400000000000091, 7.25, 12.5, 12.5]
dt=np.add.accumulate(timestep)
print len(dt)
plt.plot(dt, opm_pav/1e5, label='OPM')
plt.plot(ecl_pav.days, ecl_pav.get_values("FPR"), label='ECL', color='red')
plt.grid(True)
plt.title("FPR In OPM and ECL")
plt.legend(loc='best')
plt.xlabel("Time/Day")
plt.ylabel("FPR(bar)")
picpath="/private/miliu/data/norne/"
picname=args.en.lower() + "_fpr"  
plt.savefig(picpath+picname+".png")
print "End."
#plt.show()
