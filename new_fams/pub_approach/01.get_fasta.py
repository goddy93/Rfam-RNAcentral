import pandas as pd
import requests

EUNEWFAM_IN = "./files/df_eunewfam"  # input file
EUNEWFAM_FASTA_OUT = "./files/eunewfam.fasta"  # output file


def fasta_seq(urs_list, outfile):
    """
    Function that fetches FASTA format sequences
    from a list of RNAcentral URSs.
    """
    out_file = open(outfile, "w")
    for i in urs_list:
        url = ("http://rnacentral.org/api/v1/rna/" +
               i +
               "?format=fasta")
        req = requests.get(url, timeout=10)
        out_file.write(req.content)
    out_file.close()

# read input table
DF_EUNEWFAM = pd.read_table(
    EUNEWFAM_IN,
    low_memory=False,
    sep="\t"
    )

# make list from id column
EUNEWFAM_LIST = DF_EUNEWFAM["id"].tolist()

fasta_seq(EUNEWFAM_LIST, EUNEWFAM_FASTA_OUT)
