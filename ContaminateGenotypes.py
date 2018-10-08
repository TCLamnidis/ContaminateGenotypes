#!/projects1/tools/anaconda3/4.0.0/bin/python3

import sys, argparse, sh, random
import Utils as util

def Contaminate(Genos, SampleList, Contaminant, rates, nrReps, Index):
    Contaminated=""
    for Sample in SampleList:
        if Genos[Index[Sample]]!="9":
            for rate in rates:
                for Rep in range (nrReps):
                    if random.uniform(0,1) <= rate:
                        if Genos[Index[Contaminant]]=="1":
                            if random.uniform(0,1) <= 0.5:
                                Contaminated+="2"
                            else:
                                Contaminated+="0"
                        else:
                            Contaminated+=Genos[Index[Contaminant]]
                    else:
                        Contaminated+=Genos[Index[Sample]]
        else:
            Contaminated+="9"*nrReps*len(rates)
    return (Genos+Contaminated);

##MAIN##
parser = argparse.ArgumentParser(usage="%(prog)s (-i <INPUT FILE PREFIX>) (-o <OUTPUT FILE PREFIX>) (-s <SAMPLE>) (-c <CONTAMINANT>) (-r <RATE1,RATE2,RATE3,...>) (-n <nrReps>)" , description="A tool artificially contaminate the genotypes of multiple sample individuals with genotypes from a contaminant individual, at different rates of contamination.")
parser._optionals.title = "Available options"
parser.add_argument("-i", "--Input", type=str, metavar="<INPUT FILES PREFIX>", required=True, help="The desired input file prefix. Input files are assumed to be '<INPUT PREFIX>.geno', '<INPUT PREFIX>.snp' and '<INPUT PREFIX>.ind'.")
parser.add_argument("-o", "--Output", type=str, metavar="<OUTPUT FILES PREFIX>", required=False, help="The desired output file prefix. Three output files are created, '<OUTPUT FILES PREFIX>.geno', '<OUTPUT FILES PREFIX>.snp' and '<OUTPUT FILES PREFIX>.ind'.")
parser.add_argument("-s", "--Samples", type=str, metavar="<SAMPLE1,SAMPLE2,SAMPLE3,...>", required=True, help="The sample individual(s), whose genotypes will be contaminated.")
parser.add_argument("-c", "--Contaminant", type=str, metavar="<CONTAMINANT>", required=True, help="The contaminant individual, which will be used to contaminate the genotypes of each <SAMPLE> at the specified rate(s).")
parser.add_argument("-r", "--rates", type=str, metavar="<RATE1,RATE2,RATE3,...>", required=True, help="A comma separated list of contamination rates.")
parser.add_argument("-n", "--nrReps", type=int, metavar="<nrReps>", required=False, default=1, help="An integer value specifying the number of replicate contaminated genotypes to be created per contamination rate [1].")
args = parser.parse_args()

GenoFile = open(args.Input+".geno", "r")
SnpFile = open(args.Input+".snp", "r")
IndFile = open(args.Input+".ind", "r")

OutGenoFile = open(args.Output+".geno", "w")
OutSnpFile = args.Output+".snp"
OutIndFile = args.Output+".ind"

SampleList=[x for x in args.Samples.split(',')]
rates=[float(r) for r in args.rates.split(',')]

##Check for errors in input files
util.CheckInputFiles(args.Input)

## Index Individual in database.
(Index,Sex,Pop)=util.Indexing(args.Input, SampleList, args.Contaminant)

## Print Logfile.
with sys.stderr as o:
    print('#Input files:', args.Input+".geno", args.Input+".snp", args.Input+".ind", sep="\n\t", file=o)
    print('#Output files:', args.Output+".geno", OutSnpFile, OutIndFile, sep="\n\t", file=o)
    print('#Samples:', end="\t", file=o)
    print(*SampleList, sep=",", file=o)
    print('#Contamination Rates:', end="\t", file=o)
    print(*rates, sep=",", file=o)
    print('#NrReps:',args.nrReps, sep="\t",file=o)

##Contaminate Genotypes
for line in GenoFile:
    Genos=line.strip()
    print (Contaminate(Genos, SampleList, args.Contaminant, rates, args.nrReps, Index), file=OutGenoFile)

##Copy original .snp and .ind files
sh.cp(args.Input+".snp", OutSnpFile)
sh.cp(args.Input+".ind", OutIndFile)

##Append conaminated replicates of Samples at the end of the .ind file.
with open(OutIndFile, "a") as f:
    for Sample in SampleList:
        for rate in rates:
            for rep in range(args.nrReps):
                print (Sample+"_{}_{}".format(rate,rep+1), Sex[Sample], Pop[Sample]+"_{}".format(rate), file=f)

