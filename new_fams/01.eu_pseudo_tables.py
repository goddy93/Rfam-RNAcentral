import pandas as pd
import requests

newfam_in = "./cmscan_results/clean_tables/lato/df_newfam"
eunewfam_out = "./new_fams/files/df_eunewfam"
pseudonewfam_out = "./new_fams/files/df_pseudonewfam"

# read full new family file
df_newfam = pd.read_table(
   newfam_in,
    low_memory=False,
    sep="\t"
    )

# delete irrelevant columns
del df_newfam["rfam_acc"]
del df_newfam["hit_rfam_acc"]
del df_newfam["hit_clan_acc"]
del df_newfam["e_value"]
del df_newfam["tax_id"]

# use dictonary to tag types as bad_type (for pseudo_newfam)
df_newfam["group"] = df_newfam["rna_type"]
rnatype_group = {
    "rasiRNA":"bad_type",
    "siRNA,snRNA":"bad_type",
    "piRNA,other":"bad_type",
    "miRNA,siRNA":"bad_type",
    "miRNA,piRNA":"bad_type",
    "piRNA":"bad_type",
    "siRNA":"bad_type",
    "lncRNA":"bad_type",
    "guide_RNA":"bad_type",
    "rRNA,snRNA":"bad_type"
}
df_newfam["group"].replace(rnatype_group, inplace=True)

# make dfs: eunewfam ("real" new families) and pseudonewfam ("false" new families)
df_eunewfam = df_newfam[df_newfam.group != "bad_type"]
del df_eunewfam["group"]
df_eunewfam.reset_index(drop=True, inplace=True)

df_pseudonewfam = df_newfam[df_newfam.group == "bad_type"]
del df_pseudonewfam["group"]
df_pseudonewfam.reset_index(drop=True, inplace=True)

# save tables to csvs
df_eunewfam.to_csv(eunewfam_out, sep="\t", na_rep="None", header=True, index=False)
df_pseudonewfam.to_csv(pseudonewfam_out, sep="\t", na_rep="None", header=True, index=False)
