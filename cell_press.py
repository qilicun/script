#!/bin/env python

import numpy as np
import ert.ecl as ecl
import glob
import matplotlib.pyplot as plt
import os

import argparse
parser = argparse.ArgumentParser(description="Plot FPR for comparsion")
parser.add_argument('-f', '--fn', help='Name of opm data files', default=None, required=True)
#parser.add_argument('-f', '--fn', nargs='+', help='Name of opm data files', default=None, required=True)
parser.add_argument('-e', '--en', help='Name of ecl data files', default=None, required=True)
parser.add_argument('-m', '--mn', nargs='+', help='Global cell num', default=None, required=True)
args = parser.parse_args()

sum = ecl.EclSum(args.en)
#print sum

i, j, k = int(args.mn[0]), int(args.mn[1]), int(args.mn[2])

def get_active_index(i, j, k):
    grid = ecl.EclGrid(args.en+'.EGRID')
    active_index = grid.get_active_index( ijk=(i-1, j-1, k-1))
    return active_index

def get_opm_pav(path, cell_num):
    file = glob.glob(path+'/pressure/*.txt')
    file.sort()
    tmp=[]
    for i in file:
        p = np.loadtxt(i)
        tmp.append(np.array(p)[cell_num])
    return np.array(tmp)
#cell_num.append(get_active_index(99892))
#cell_num.append(get_active_index(11462))


print "Starting plot cell pressure\n"
cell_num = get_active_index(i, j, k)
print "Active cell index: ", cell_num
opm_pav = get_opm_pav(args.fn, cell_num)

#load ecl result
ecl_time= sum.days
ecl_pav = sum.get_values("BPR:"+args.mn[0]+","+args.mn[1]+","+args.mn[2])
#set fixed time step
timestep=[0]+[1,2,3,4,5,5,10,10]+[20]*3+[25]*8#+[50]*34#+[100]*80
#dt=np.add.accumulate(timestep)

#timestep =[0, 1.0, 1.0, 1.0, 1.5, 1.5, 4.0, 5.0, 5.0, 5.0, 5.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2.0, 2.5, 3.9099999999999966, 5.7900000000000063, 5.7999999999999972, 12.5, 12.5, 12.5, 12.5, 25.0, 2.5, 3.1200000000000045, 4.8899999999999864, 7.2400000000000091, 7.25, 12.5, 12.5, 25.0, 2.5, 3.1200000000000045, 4.8899999999999864, 7.2400000000000091, 7.25, 12.5, 12.5]
dt=np.add.accumulate(timestep)
plt.plot(dt, opm_pav/1e5, label='OPM')
plt.plot(ecl_time, ecl_pav, label='ECL', color='red')
plt.grid(True)
cell_name=args.mn[0]+","+args.mn[1]+","+args.mn[2]
title = "Cell " + cell_name + " Pressure In OPM and ECL"
plt.title(title)
plt.legend(loc='best')
plt.xlabel("Time(Day)")
plt.ylabel("PRESSURE(Bar)")
picpath="/private/miliu/data/norne/"
picname=args.en.lower()+ "_cell_"+cell_name
plt.savefig(picpath+picname+".png")
#plt.show()
print "End"
