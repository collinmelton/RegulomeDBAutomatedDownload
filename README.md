# RegulomeDBAutomatedDownload
This repository contains code to enable automate the downloading of RegulomeDB annotations from a tsv source file.

run as follows:
python AnnotateWithRegulomeDB.py --I input.tsv --O output.RegDB


the default input file format is as follows:

\#
\# exactly 3 rows without data including col names row below, this is a tab delimited file
chrom pos
1	120001
3	150002
