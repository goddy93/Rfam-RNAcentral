import requests
import pandas as pd
import sys

TSV_IN = sys.argv[1]  # one column .tsv file with urs
FASTA_OUT = sys.argv[2]  # fasta file output

# .............FUNCTIONS.............


def tabletolist(tsvtbl):
    """
    Takes single column tsv and makes it
    a list
    """
    urs_df = pd.read_table(
               tsvtbl,
               header=None)
    urs_list = urs_df[0].tolist()
    return urs_list


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
        req = requests.get(url, timeout=30)
        out_file.write(req.content)
    out_file.close()

# .............PROCESS.............
fasta_seq(tabletolist(TSV_IN), FASTA_OUT)
