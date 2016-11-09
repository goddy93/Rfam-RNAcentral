import sys
import Bio
from Bio import SeqIO

filename= sys.argv[1]
for rec in SeqIO.parse(filename, "fasta"):
    name = rec.id
    seq = rec.seq
    seqLen = len(rec)
    print name, seqLen