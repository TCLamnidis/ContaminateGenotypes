#!/projects1/tools/anaconda3/4.0.0/bin/python3
import sys, argparse, sh, random
import Utils as util

def SprinkleMissing(Genos, SampleList, rates, nrReps, Index):
    Missing=""
    for Sample in SampleList:
        if Genos[Index[Sample]]!="9":
            for rate in rates:
                for Rep in range (nrReps):
                    if random.uniform(0,1) <= rate:
                        Missing+="9"
                    else:
                        Missing+=Genos[Index[Sample]]
        else:
            Missing+="9"*nrReps*len(rates)
    return (Genos+Missing)

## MAIN ##
parser = argparse.ArgumentParser(usage="%(prog)s (-i <INPUT FILE PREFIX>) (-o <OUTPUT FILE PREFIX>) (-s <SAMPLE>) (-r <RATE1,RATE2,RATE3,...>) (-n <nrReps>)" , description="A tool artificially sprinkle missing data in the genotypes of multiple sample individuals at different missingness rates.")
parser._optionals.title = "Available options"
parser.add_argument("-i", "--Input", type=str, metavar="<INPUT FILES PREFIX>", required=True, help="The desired input file prefix. Input files are assumed to be '<INPUT PREFIX>.geno', '<INPUT PREFIX>.snp' and '<INPUT PREFIX>.ind'.")
parser.add_argument("-o", "--Output", type=str, metavar="<OUTPUT FILES PREFIX>", required=False, help="The desired output file prefix. Three output files are created, '<OUTPUT FILES PREFIX>.geno', '<OUTPUT FILES PREFIX>.snp' and '<OUTPUT FILES PREFIX>.ind'.")
parser.add_argument("-s", "--Samples", type=str, metavar="<SAMPLE1,SAMPLE2,SAMPLE3,...>", required=True, help="The sample individual(s), whose genotypes will go missing.")
parser.add_argument("-r", "--rates", type=str, metavar="<RATE1,RATE2,RATE3,...>", required=True, help="A comma separated list of missingness rates.")
parser.add_argument("-n", "--nrReps", type=int, metavar="<nrReps>", required=False, default=5, help="An integer value specifying the number of replicate individuals to be created per missingness rate [5].")
args = parser.parse_args()

GenoFile = open(args.Input+".geno", "r")
SnpFile = open(args.Input+".snp", "r")
IndFile = open(args.Input+".ind", "r")

OutGenoFile = open(args.Output+".geno", "w")
OutSnpFile = args.Output+".snp"
OutIndFile = args.Output+".ind"

SampleList=[x for x in args.Samples.split(',')]
rates=[float(r) for r in args.rates.split(',')]

## Check for errors in input files.
util.CheckInputFiles(args.Input)

## Index Individual in database.
(Index,Sex,Pop)=util.Indexing(args.Input, SampleList, '')

## Sprinkle missing genotypes in data.
for line in GenoFile:
    Genos=line.strip()
    print (SprinkleMissing(Genos, SampleList, rates, args.nrReps, Index), file=OutGenoFile)

##Copy original .snp and .ind files
sh.cp(args.Input+".snp", OutSnpFile)
sh.cp(args.Input+".ind", OutIndFile)

##Append conaminated replicates of Samples at the end of the .ind file.
with open(OutIndFile, "a") as f:
    for Sample in SampleList:
        for rate in rates:
            for rep in range(args.nrReps):
                print (Sample+"_m{}_{}".format(rate,rep+1), Sex[Sample], Pop[Sample]+"_m{}".format(rate), file=f)

