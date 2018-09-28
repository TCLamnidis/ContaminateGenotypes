import sys, argparse, sh, random

def Indexing (Input, SampleList, Contaminant):
    Index={}
    Sex={}
    Pop={}
    Targets="{}\|"*(len(SampleList))
    Targets+="{}"
    for line in sh.grep(sh.cat("-n",Input+".ind"), Targets.format(*SampleList,Contaminant),_ok_code=[0,1]):
        fields=line.strip().split()
        if fields[1] in SampleList or fields[1] == Contaminant:
            Index[fields[1]]=(int(fields[0]) -1)
            Sex [fields[1]]=fields[2]
            Pop [fields[1]]=fields[3]
    return (Index, Sex, Pop);

def CheckInputFiles(Input):
    ##Check geno and snp compatibility
    lineNo = ""
    for line in sh.grep(sh.wc("-l", Input+".geno", Input+".snp"), Input):
        if lineNo=="":
            lineNo=line.strip().split()[0]
        elif lineNo==line.strip().split()[0]:
            break
        elif lineNo!=line.strip().split()[0]:
            raise IOError("Input .snp and .geno files do not match.")

    ##Check geno and ind compatibility
    with open(Input+".geno", "r") as f:
        for line in f:
            if str(len(line.strip())) == sh.wc("-l", Input+".ind").strip().split()[0]:
                break
            else:
                raise IOError("Input .ind and .geno files do not match.");
