import sys
from Bio import SeqIO
import pandas as pd

input_file = sys.argv[1]
output_file = input_file + "_seq-ids.txt"

ids = []

for x in SeqIO.parse(input_file, "fasta"):
	ids.append(x.id)

df=pd.DataFrame(columns = ["id"])
df["id"] = ids

df.to_csv(output_file, sep = '\t', index = False)