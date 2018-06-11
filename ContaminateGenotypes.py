#!/usr/bin/env python3

import sys, argparse, sh, random

def Indexing (Sample, Contaminant):
    Index={}
    Sex={}
    Pop={}
    for line in sh.grep(sh.cat("-n",args.Input+".ind"), "{}\|{}".format(Sample,Contaminant),_ok_code=[0,1]):
        fields=line.strip().split()
        if fields[1] == Sample or fields[1] == Contaminant:
            Index[fields[1]]=(int(fields[0]) -1)
            Sex [fields[1]]=fields[2]
            Pop [fields[1]]=fields[3]
    return (Index, Sex, Pop)

def Contaminate(Genos, Sample, Contaminant, rates, nrReps, Index):
    Contaminated=""
    if Genos[Index[Sample]]!="9":
        for rate in rates:
            for Rep in range (nrReps):
                if random.uniform(0,1) <= rate:
                    Contaminated+=Genos[Index[Contaminant]]
                else:
                    Contaminated+=Genos[Index[Sample]]
    else:
        Contaminated+="9"*nrReps*len(rates)
    return (Genos+Contaminated)
    
parser = argparse.ArgumentParser(usage="%(prog)s (-i <INPUT FILE PREFIX>) (-o <OUTPUT FILE PREFIX>) (-s <SAMPLE>) (-c <CONTAMINANT>) (-r <RATE1,RATE2,RATE3,...>) (-n <nrReps>)" , description="A tool to check two different EingenStrat databses for shared individuals, and extract or remove individuals from an EigenStrat database.")
parser._optionals.title = "Available options"
parser.add_argument("-i", "--Input", type=str, metavar="<INPUT FILES PREFIX>", required=True, help="The desired input file prefix. Input files are assumed to be '<INPUT PREFIX>.geno', '<INPUT PREFIX>.snp' and '<INPUT PREFIX>.ind'.")
parser.add_argument("-o", "--Output", type=str, metavar="<OUTPUT FILES PREFIX>", required=False, help="The desired output file prefix. Three output files are created, '<OUTPUT FILES PREFIX>.geno', '<OUTPUT FILES PREFIX>.snp' and '<OUTPUT FILES PREFIX>.ind'.")
parser.add_argument("-s", "--Sample", type=str, metavar="<SAMPLE>", required=True, help="The sample individual, whose genotypes will be contaminated.")
parser.add_argument("-c", "--Contaminant", type=str, metavar="<CONTAMINANT>", required=True, help="The contaminant individual, which will be used to contaminate the genotypes of <SOURCE> at the specified rate(s).")
parser.add_argument("-r", "--rates", type=str, metavar="<RATE1,RATE2,RATE3,...>", required=True, help="A comma separated list of contamination rates.")
parser.add_argument("-n", "--nrReps", type=int, metavar="<nrReps>", required=False, default=5, help="An integer value specifying the number of replicate contaminated genotypes to be created per contamination rate [5].")
args = parser.parse_args()

GenoFile = open(args.Input+".geno", "r")
SnpFile = open(args.Input+".snp", "r")
IndFile = open(args.Input+".ind", "r")

OutGenoFile = open(args.Output+".geno", "w")
OutSnpFile = args.Output+".snp"
OutIndFile = args.Output+".ind"

rates=[float(r) for r in args.rates.split(',')]

#Check for errors in input files
##Check geno and snp compatibility
lineNo = ""
for line in sh.grep(sh.wc("-l", args.Input+".geno", args.Input+".snp"), args.Input):
    if lineNo=="":
        lineNo=line.strip().split()[0]
    elif lineNo==line.strip().split()[0]:
        break
    elif lineNo!=line.strip().split()[0]:
        raise IOError("Input .snp and .geno files do not match.")

##Check geno and ind compatibility
with open(args.Input+".geno", "r") as f:
    for line in f:
        if str(len(line.strip())) == sh.wc("-l", args.Input+".ind").strip().split()[0]:
            break
        else:
            raise IOError("Input .ind and .geno files do not match.")
(Index,Sex,Pop)=Indexing(args.Sample, args.Contaminant)
for line in GenoFile:
    Genos=line.strip()
    print (Contaminate(Genos, args.Sample, args.Contaminant, rates, args.nrReps, Index), file=OutGenoFile)

sh.cp(args.Input+".snp", OutSnpFile)
sh.cp(args.Input+".ind", OutIndFile)
with open(OutIndFile, "a") as f:
    for rate in rates:
        for rep in range(args.nrReps):
            print (args.Sample+"_{}_{}".format(rate,rep+1), Sex[args.Sample], Pop[args.Sample]+"_{}".format(rate), file=f)

