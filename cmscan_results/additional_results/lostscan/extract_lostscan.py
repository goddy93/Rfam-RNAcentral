# cd /Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/cmscan_results
import pandas as pd
import numpy as np

# --LOAD FILES--
DF_LOSTSCAN = pd.read_table(
    "./query_files/query_lostscan",
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


# lostscan
len(DF_LOSTSCAN["id"])
len(set(DF_LOSTSCAN["id"]))

# ..counts..
type_count = DF_LOSTSCAN["rna_type"].value_counts()
fam_count = DF_LOSTSCAN["rfam_acc"].value_counts()
db_count = DF_LOSTSCAN["db"].value_counts()

(DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00017")])["rna_type"].value_counts()



(DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00177")])["db"].value_counts()

(DF_LOSTSCAN[(DF_LOSTSCAN.rna_type == "SRP_RNA")])["db"].value_counts()
(DF_LOSTSCAN[(DF_LOSTSCAN.rna_type == "hammerhead")])["rfam_acc"].value_counts()

SRP = (DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00017")])
(SRP[(SRP.tax_id == "30608")])

(DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00005")])["rna_type"].value_counts()
(DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00005")])["tax_id"].value_counts()
(DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00428")])["rna_type"].value_counts()

(DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00177")])["rna_type"].value_counts()



len((DF_LOSTSCAN[(DF_LOSTSCAN.rfam_acc == "RF00017")]))
len((DF_NEWMEM[(DF_NEWMEM.rfam_acc == "RF00017")]))
len((DF_NEWFAM[(DF_NEWFAM.rfam_acc == "RF00017")]))


a.to_csv("/Users/nquinones/Desktop/tax17.tsv", sep="\t", index=True)
SRP.to_csv("/Users/nquinones/Desktop/SRP.tsv", sep="\t", index=False)
