import pandas as pd
import requests

eunewfam_in = "./files/df_eunewfam"
pseudonewfam_in = "./files/df_pseudonewfam"
eunewfam_fasta_out = "./files/eunewfam.fasta"
pseudonewfam_fasta_out = "./files/pseudonewfam.fasta"

# read full new family file
df_eunewfam = pd.read_table(
  eunewfam_in,
  low_memory=False,
  sep="\t"
  )

df_pseudonewfam = pd.read_table(
  pseudonewfam_in,
  low_memory=False,
  sep="\t"
  )

# make lists with urs
eunewfam_list = df_eunewfam["id"].tolist()
pseudonewfam_list = df_pseudonewfam["id"].tolist()

# make FASTA file with all the sequences in a list


def fasta_seq(urs_list, outfile):
    f = open(outfile, "w")
    for i in urs_list:
        url = "http://rnacentral.org/api/v1/rna/"+i+"?format=fasta"
        r = requests.get(url, timeout=10)
        f.write(r.content)
    f.close()

# run function for both lists
fasta_seq(eunewfam_list, eunewfam_fasta_out)
# fasta_seq(pseudonewfam_list, pseudonewfam_fasta_out)
