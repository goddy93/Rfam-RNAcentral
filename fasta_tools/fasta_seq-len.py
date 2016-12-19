import sys
from Bio import SeqIO
import pandas as pd

input_file = sys.argv[1]
output_file = input_file + "_seq-len.txt"

ids = []
seq_len = []

for x in SeqIO.parse(input_file, "fasta"):
	ids.append(x.id)
	seq_len.append(len(x))

df=pd.DataFrame(columns = ["id", "length"])
df["id"] = ids
df["length"] = seq_len

df.to_csv(output_file, sep = '\t', index = False)
