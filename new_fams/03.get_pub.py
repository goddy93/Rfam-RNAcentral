import pandas as pd
import requests

EUNEWFAM_IN = "./files/df_eunewfam"  # input file
EUNEWFAM_PUB_OUT = "./files/eunewfam.pub"  # output file


def pubmed_id(urs_list, page_size, time_out):
    """
    Function that creates tab delimited file with publication ids
    (pubmed_id and pub_id) per reference, for a list of RNAcentral URSs.
    """
    out_file = open(EUNEWFAM_PUB_OUT, "w")
    # write header
    out_file.write("URS\tpubmed_id\tpub_id\n")
    # request from RNAcentral, write into file or indicate error
    for i in urs_list:
        url = ("http://rnacentral.org/api/v1/rna/" +
               i +
               "/publications?page_size=" +
               str(page_size))
        # write into file (show err if timeout, or results exceed page length)
        try:
            req = requests.get(url, timeout=time_out)
            data = req.json()
            num_ref = len(data["results"])
            for j in range(0, num_ref):
                pubmed = str(data['results'][j]["pubmed_id"])
                pubid = str(data['results'][j]["pub_id"])
                out_file.write(i + "\t" +
                               pubmed +
                               "\t" +
                               pubid +
                               "\n")
            if num_ref != data["count"]:
                out_file.write(i +
                               "\terr(" +
                               str(page_size) +
                               "+)\terr(" +
                               str(page_size) +
                               "+)\n")
        except requests.exceptions.Timeout:
            out_file.write(i+"\terr(timeout)\terr(timeout)\n")
    out_file.close()

# read input table
DF_EUNEWFAM = pd.read_table(
    EUNEWFAM_IN,
    low_memory=False,
    sep="\t"
    )

# make list from id column
EUNEWFAM_LIST = DF_EUNEWFAM["id"].tolist()
EUNEWFAM_LIST = EUNEWFAM_LIST[0:10]

# input function args
PAGE_LENGTH = 50  # results to be checked from RNAcentral API, max 100
TIME_OUT_IN = 10  # in seconds

pubmed_id(EUNEWFAM_LIST, PAGE_LENGTH, TIME_OUT_IN)
