# ContaminateGenotypes
A simple python script to contaminate Eigenstrat genotypes. 

A tool artificially contaminate the genotypes of multiple sample individuals 
with genotypes from a contaminant individual, at different rates of contamination.

```
Available options:
  -h, --help            show this help message and exit
  -i <INPUT FILES PREFIX>, --Input <INPUT FILES PREFIX>
                        The desired input file prefix. Input files are assumed
                        to be '<INPUT PREFIX>.geno', '<INPUT PREFIX>.snp' and
                        '<INPUT PREFIX>.ind'.
  -o <OUTPUT FILES PREFIX>, --Output <OUTPUT FILES PREFIX>
                        The desired output file prefix. Three output files are
                        created, '<OUTPUT FILES PREFIX>.geno', '<OUTPUT FILES
                        PREFIX>.snp' and '<OUTPUT FILES PREFIX>.ind'.
  -s <SAMPLE1,SAMPLE2,SAMPLE3,...>, --Samples <SAMPLE1,SAMPLE2,SAMPLE3,...>
                        The sample individual, whose genotypes will be
                        contaminated.
  -c <CONTAMINANT>, --Contaminant <CONTAMINANT>
                        The contaminant individual, which will be used to
                        contaminate the genotypes of each <SAMPLE> at the
                        specified rate(s).
  -r <RATE1,RATE2,RATE3,...>, --rates <RATE1,RATE2,RATE3,...>
                        A comma separated list of contamination rates.
  -n <nrReps>, --nrReps <nrReps>
                        An integer value specifying the number of replicate
                        contaminated genotypes to be created per contamination
                        rate [1].
  -v, --overlapOnly     When provided, only SNPs that are present in both
                        Contaminant and Sample will be contaminated, while all
                        other SNPs will be set to missing. This ensures
                        conaminant genotypes will not be diluted due to lack
                        of coverage overlap in the Sample and Contaminant.
```
The provided script will contaminate the genotypes of a given sample individual 
in an Eigenstrat dataset at a specified rate, to match the genotypes of a 
specified contaminant individual. Missing data in the sample individual will be 
kept as missing. Heterozygotes in the contaminant will be pseudohaploidised. A 
number of replicates can be specified for each contamination rate. Contaminated 
individuals will be saved as a separate individual within the resulting 
Eigenstrat database, following the naming scheme ``Sample_ContaminationRate_ReplicateNumber``. 
The population assigned to each replicate follows a similar naming scheme, but without a replicate number.

In cases where the contaminant individual has a missing genotype, the default behaviour is to add missing genotypes at the specified contamination rate. The ``-v/--overlapOnly`` option can be provided to override this default and set all genotypes that are missing in **either the sample or contaminant** to missing. In cases where both the sample and contaminant have incomplete coverage (as is often the case with ancient individuals), this will lower overall coverage, but keep result contamination rates consistent.
