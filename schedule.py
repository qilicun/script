#!/bin/env python
#
# Author: miliu - miliu@statoil.com
#
# Last modified:	2014-09-19 10:27
#
# Description: generate schedule file for eclipse and cmg 

import numpy as np
import re
import argparse
import os

parser = argparse.ArgumentParser(description="Plot FPR for comparsion")
parser.add_argument('-f', '--filen', help='Name of lab data files', default=None, required=True)
parser.add_argument('-t', '--type', help='Tyep of Simulator(ecl or cmg)', default="ecl", required=True)
parser.add_argument('-o', '--output', help='Name of schedule', default="schedule.inc", required=False)
args = parser.parse_args()

class Ecl:
    def __init__(self):
        print "ecl schedule!\n"
    def welspecs(self, inje_pos, file):
        file.write("\nwelspecs".upper()+"\n")
        inje = "'I'  'G' "+str(inje_pos) + "  1  1*  'WAT'  0.0  'STD'  'SHUT'  'NO' /"
        prod = "'P'  'G'   1  1  1*  'OIL'  0.0  'STD'  'SHUT'  'NO' /"
        file.write(inje)
        file.write("\n")
        file.write(prod)
        file.write("\n/\n")

    def compdat(self, inje_pos, file):
        file.write("\ncompdat".upper()+"\n")
        inje="'I'   "+str(inje_pos)+"   1   1   1 'OPEN'   0  .0   0.05 /"
        prod="'P'   1     1   1   1 'OPEN'   0  .0   0.05 /"
        file.write(inje)
        file.write("\n")
        file.write(prod)
        file.write("\n/\n")

    def wconhist(self, orat, wrat, file):
        file.write("\nwconhist".upper()+"\n")
        prod="'P' 'OPEN' 'BHP' "+str(orat)+"  "+str(wrat)+"  4*  10  /"
        file.write(prod)
        file.write("\n/\n")

    def wconinjh(self, wrat, bhp, file):
        file.write("\nwconinjh".upper()+"\n")
        item="'I' 'WAT' 'OPEN'   "+str(wrat)+"   " +str(bhp)+"   6* 'RATE'/"
        file.write(item)
        file.write("\n/\n")

    def wpolymer(self, amount, file):
        file.write("\nwpolymer".upper()+"\n")
        item="'I'   " + str(amount) + "   0.0   /"
        file.write(item)
        file.write("\n/\n")

class Parser:
    def __init__(self, filen):
        self.dm={}
        self.data=[]
        self.string=""
        self.filetype="ECLIPSE"
        self.stype="SS"
        with open(filen, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not len(line):
                    continue
                if re.match("^-", line):
                    continue
                if re.match("^/", line):
                    continue
                pattern = '[a-zA-Z]'
                if re.match(pattern, line):
                    self.string = line
                    continue
                line = line.split()
                if line[-1] != "/":
                    self.data += line
                else:
                    self.data += line[0:-1]
                    self.dm[self.string] = self.data
                    self.data = []

    def get_data(self):
        return self.dm

    def get_filetype(self):
        self.filetype=dm["filetype"]
        return self.filetype

    def get_simulation_type(self):
        self.stype=dm["simulationtype"]
        return self.stype

class Cmg:
    def __init__(self):
        print "create cmg schedule\n"

    def wellName(self, name, file):
        file.write("WELL  "+ "'"+str(name)+"'\n")

    def polyMoleFrac(self, pm, con):
        return con/1e6/pm/(con/1e6/pm + (1-con/1e6)/18)

    def injeConfig(self, pos, rate, poly_mole_frac, file):
        file.write("IJNECTOR UNWEIGHT 'I'\n")
        file.write("INCOMP  WATER "+str((1.-poly_mole_frac))+" "+str(poly_mole_frac)+" 0.0\n")
        file.write("OPERATE  MAX  STW  "+str(rate)+"  CONT  REPEAT\n")
        file.write("PERF  WI  'I'\n")
        file.write("\t"+str(pos[0])+"  "+str(pos[1])+"  "+str(pos[2])+"  2.63  OPEN  FLOW-FROM  'SURFACE'   REFLAYER\n")
    
    def injector(self, rate, poly_mole_frac, file):
        file.write("IJNECTOR UNWEIGHT 'I'\n")
        file.write("INCOMP  WATER "+str((1.-poly_mole_frac))+" "+str(poly_mole_frac)+" 0.0\n")
        file.write("OPERATE  MAX  STW  "+str(rate)+"  CONT  REPEAT\n")

    def prodConfig(self, pos, bhp, file):
        file.write("PRODUCER   'P'\n")
        file.write("OPERATE  MIN  BHP  "+str(bhp)+"\n")
        file.write("GEOMETRY  I  0.1  0.235  1.  0.\n")
        file.write("PERF  GEOA  'P'\n")
        file.write("\t"+str(pos[0])+"  "+str(pos[1])+"  "+str(pos[2])+"  1.  OPEN  FLOW-TO  'SURFACE'   REFLAYER\n")

class Schedule:
    def __init__(self, filen, name):
        if os.path.exists(os.path.abspath(name)):
            os.remove(name)
        self.file=file(name, 'a+')
        self.parser=Parser(filen)

    def writeEcl(self):
        self.ecl=Ecl()
        dm = self.parser.get_data()
        injecting=np.array(dm["EXPERIMENT"]).reshape(len(dm["EXPERIMENT"])/6,6)
        self.ecl.welspecs(dm["DIMENSION"][0], self.file)
        self.ecl.compdat(dm["DIMENSION"][0], self.file)
        for i in range(len(injecting[:,0])):
            if float(injecting[:,0][i]) != 0.0:
                self.file.write(str(injecting[:,0][i]))
                self.file.write("\n/\n")
            self.ecl.wconhist(injecting[:,3][i], injecting[:,3][i], self.file)
            self.ecl.wconinjh(injecting[:,1][i],float(dm["PRESSURE"][0])+float(injecting[:,5][i]), self.file)
            self.ecl.wpolymer(float(injecting[:,2][i])/1e6,self.file)
            j=float(injecting[:,0][i])
            if i != (len(injecting[:,0])-1):
                self.file.write("\nTIME\n")
                start=float(injecting[:,0][i])
                stop=float(injecting[:,0][i+1])
                n=int((stop-start)/0.2)
                for j in range(n-1):
                    self.file.write(str(start+(j+1)*0.2)+"\n")
            else:
                self.file.write("\nEND\n")

    def writeCmg(self):
        self.cmg=Cmg()
        dm = self.parser.get_data()
        data=np.array(dm["EXPERIMENT"]).reshape(len(dm["EXPERIMENT"])/6,6)
        for i in range(len(data[:,0])):
            if float(data[:,0][i]) == 0.0:
                self.file.write("\nTIME  "+str(float(data[:,0][i])*60)+"\n\n")
                self.file.write("\nDTWELL  15\n")
                self.cmg.wellName("I", self.file)
                pmf = self.cmg.polyMoleFrac(float(dm["POLYMERMW"][0]), float(data[:,2][i]))
                self.cmg.injeConfig(dm["DIMENSION"], float(data[:,1][i])/60, pmf, self.file)
                self.cmg.wellName("P", self.file)
                self.cmg.prodConfig(dm["DIMENSION"], float(dm["PRESSURE"][0])*101.3, self.file)
            if i != (len(data[:,0])-1):
                start=float(data[:,0][i])
                stop=float(data[:,0][i+1])
                n=int((stop-start)/0.2)
                for j in range(n-1):
                    self.file.write("\nTIME  "+str((start+(j+1)*0.2)*60))
                self.file.write("\nTIME  "+ str(float(data[:,0][i+1])*60)+"\n\n")
                pmf = self.cmg.polyMoleFrac(float(dm["POLYMERMW"][0]), float(data[:,2][i+1]))
                self.cmg.injector(float(data[:,1][i+1])/60, pmf, self.file)
            else:
                self.file.write("\nSTOP\n\n")
if __name__=='__main__':
    schedule=Schedule(args.filen, args.output)
    if args.type == "ecl" or args.type == "ECL":
        schedule.writeEcl()
    if args.type == "cmg" or args.type == "CMG":
        schedule.writeCmg()
