# ContaminateGenotypes
A simple python script to contaminate Eigenstrat genotypes. 

A tool to check two different EingenStrat databses for shared individuals, and
extract or remove individuals from an EigenStrat database.

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
  -s <SAMPLE>, --Sample <SAMPLE>
                        The sample individual, whose genotypes will be
                        contaminated.
  -c <CONTAMINANT>, --Contaminant <CONTAMINANT>
                        The contaminant individual, which will be used to
                        contaminate the genotypes of <SOURCE> at the specified
                        rate(s).
  -r <RATE1,RATE2,RATE3,...>, --rates <RATE1,RATE2,RATE3,...>
                        A comma separated list of contamination rates.
  -n <nrReps>, --nrReps <nrReps>
                        An integer value specifying the number of replicate
                        contaminated genotypes to be created per contamination
                        rate [5].
```
The provided script will contaminate the genotypes of a given sample individual in an Eigenstrat dataaset at a specified rate, to match the genotypes of a specified contaminant individual. 
Missing data in the sample individual will be kept as missing. A number of replicates can be specified for each contamination rate. contaminated individuals will be saved as a separate individual within the resulting Eigenstrat database, following the naming scheme ``Sample_ContaminationRate_ReplicateNumber``. The population assigned to each replicate follows a similar naming scheme, but without a replicate number.
