import pandas as pd
import numpy as np

DF_NEWFAM = pd.read_table(
    "./query_files/query_newfam",
    sep="\t",
    low_memory=False,
    names=["id",
           "len",
           "db",
           "rna_type",
           "rfam_acc",
           "tax_id",
           "hit_rfam_acc",
           "hit_clan_acc",
           "e_value"]
    )


len((DF_NEWFAM[(DF_NEWFAM.rna_type == "tRNA")]))
len((DF_NEWFAM[(DF_NEWFAM.rna_type == "rRNA")]))
len((DF_NEWFAM[(DF_NEWFAM.rna_type == "tmRNA")]))

(DF_NEWFAM[(DF_NEWFAM.rna_type == "tRNA")])["db"].value_counts()
(DF_NEWFAM[(DF_NEWFAM.rna_type == "tRNA")])["len"].describe()


tRNA = (DF_NEWFAM[(DF_NEWFAM.rna_type == "tRNA")])
(tRNA[(tRNA.len < 20)])
(tRNA[(tRNA.len > 1000)])

(DF_NEWFAM[(DF_NEWFAM.rna_type == "tRNA")])["tax_id"].value_counts()