import pandas as pd
import numpy as np

IN_SAMEHIT = "./query_files/query_samehit"
IN_CONFHIT = "./query_files/query_confhit"
IN_LOSTSCAN = "./query_files/query_lostscan"
IN_NEWMEM = "./query_files/query_newmem"
IN_NEWFAM = "./query_files/query_newfam"

OUT_DF_RNATYPE = "./additional_results/all_rnatype.csv"
OUT_BIG_TABLE = "./additional_results/rnatype_family.csv"

DF_SAMEHIT = pd.read_table(
    IN_SAMEHIT,
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

DF_CONFHIT = pd.read_table(
    IN_CONFHIT,
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

DF_LOSTSCAN = pd.read_table(
    IN_LOSTSCAN,
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

DF_NEWMEM = pd.read_table(
    IN_NEWMEM,
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

DF_NEWFAM = pd.read_table(
    IN_NEWFAM,
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

DF_IN = pd.concat([DF_SAMEHIT, DF_CONFHIT, DF_LOSTSCAN, DF_NEWMEM, DF_NEWFAM])

DF_RNATYPE = pd.DataFrame(DF_IN["rna_type"].value_counts())
DF_RNATYPE.reset_index(level=0, inplace=True)
DF_RNATYPE.columns = ['rna_type', 'count']
DF_RNATYPE["in_rfam"] = np.nan

BIG_TABLE = pd.DataFrame()
for i in DF_RNATYPE["rna_type"]:
    a = DF_IN[DF_IN["rna_type"] == i]
    family = pd.DataFrame(a["rfam_acc"].value_counts())
    family.reset_index(level=0, inplace=True)
    family.columns = ["family", "count"]
    family.insert(0, "rna_type", i)
    BIG_TABLE = BIG_TABLE.append(family)

for i in DF_RNATYPE["rna_type"]:
    inrfam = (BIG_TABLE[BIG_TABLE["rna_type"] == i])["count"].sum()
    test = DF_RNATYPE['rna_type'] == i
    index = test[test].index.tolist()
    index = index[0]
    DF_RNATYPE["in_rfam"].loc[index] = inrfam

DF_RNATYPE.to_csv(
    OUT_DF_RNATYPE,
    sep="\t",
    na_rep="None",
    header=True,
    index=False)

BIG_TABLE.to_csv(
    OUT_BIG_TABLE,
    sep="\t",
    na_rep="None",
    header=True,
    index=False)
