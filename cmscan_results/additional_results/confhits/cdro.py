import pandas as pd
import numpy as np

IN_SAMEHIT = "./query_files/query_samehit"
IN_CONFHIT = "./query_files/query_confhit"
QUERY_COLAPSEDHITS = "./query_files/query_colapsedhits"

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

DF_COLAPSEDHITS = pd.read_table(
    QUERY_COLAPSEDHITS,
    sep="\t",
    names=["id", "families"]
    )

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

DF_NEWMEM = pd.read_table(
    "./query_files/query_newmem",
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

# samehit
len(DF_SAMEHIT["id"])
len(set(DF_SAMEHIT["id"]))
# ..intersections..
len(set(DF_SAMEHIT["id"]).intersection(set(DF_CONFHIT["id"])))
len(set(DF_SAMEHIT["id"]).intersection(set(DF_LOSTSCAN["id"])))
len(set(DF_SAMEHIT["id"]).intersection(set(DF_NEWFAM["id"])))
len(set(DF_SAMEHIT["id"]).intersection(set(DF_NEWFAM["id"])))


# confhit
len(DF_CONFHIT["id"])
len(set(DF_CONFHIT["id"]))
# ..intersections..
len(set(DF_CONFHIT["id"]).intersection(set(DF_SAMEHIT["id"])))
len(set(DF_CONFHIT["id"]).intersection(set(DF_LOSTSCAN["id"])))
len(set(DF_CONFHIT["id"]).intersection(set(DF_NEWMEM["id"])))
len(set(DF_CONFHIT["id"]).intersection(set(DF_NEWFAM["id"])))

# lostscan
len(DF_LOSTSCAN["id"])
len(set(DF_LOSTSCAN["id"]))

# newmem
len(DF_NEWMEM["id"])
len(set(DF_NEWMEM["id"]))
# ..repeated..
newmem_count = DF_NEWMEM["id"].value_counts()
newmem_rep = newmem_count[newmem_count > 1]

# newfam
len(DF_NEWFAM["id"])
len(set(DF_NEWFAM["id"]))

# find urs with multiple annotations
ANNOT = pd.DataFrame(DF_CONFHIT["rfam_acc"].value_counts())
MULT_ANNOT = DF_CONFHIT[(DF_CONFHIT.rfam_acc == "RF02541,RF02540") |
                        (DF_CONFHIT.rfam_acc == "RF02540,RF02541") |
                        (DF_CONFHIT.rfam_acc == "RF00177,RF01959") |
                        (DF_CONFHIT.rfam_acc == "RF01959,RF00177") |
                        (DF_CONFHIT.rfam_acc == "RF02540,RF02543") |
                        (DF_CONFHIT.rfam_acc == "RF02541,RF02543") |
                        (DF_CONFHIT.rfam_acc == "RF01960,RF02542") |
                        (DF_CONFHIT.rfam_acc == "RF02542,RF01960") |
                        (DF_CONFHIT.rfam_acc == "RF00177,RF02542") |
                        (DF_CONFHIT.rfam_acc == "RF02540,RF02541,RF02543") |
                        (DF_CONFHIT.rfam_acc == "RF02543,RF02541")
                        ]
len(set(MULT_ANNOT["id"]))
len(set(MULT_ANNOT["id"]).intersection(set(DF_CONFHIT["id"])))
len(set(MULT_ANNOT["id"]).intersection(set(DF_SAMEHIT["id"])))

# find urs with multiple hits
MASK = (DF_COLAPSEDHITS['families'].str.len() > 7)
MULT_HITS = DF_COLAPSEDHITS.loc[MASK]

only_conf = set(DF_CONFHIT["id"])- set(DF_SAMEHIT["id"])
only_inter = set(DF_SAMEHIT["id"]).intersection(set(DF_CONFHIT["id"]))
only_same = set(DF_SAMEHIT["id"]) - set(DF_CONFHIT["id"])

len(set(MULT_HITS["id"]))
len(set(only_conf).intersection(set(MULT_HITS["id"])))
len(set(only_inter).intersection(set(MULT_HITS["id"])))
len(set(only_same).intersection(set(MULT_HITS["id"])))
len(set(DF_NEWMEM["id"]).intersection(set(MULT_HITS["id"])))

set(only_conf) - set(MULT_ANNOT["id"]) - set(MULT_HITS["id"])

# conf_single 40
only_conf_sing = set(only_conf) - set(MULT_ANNOT["id"]) - set(MULT_HITS["id"])
DF_CONF_SING = DF_CONFHIT[DF_CONFHIT["id"].isin(only_conf_sing)]
DF_CONF_SING.to_csv("/Users/nquinones/Desktop/40.tsv", sep="\t", index=False)
# conf_part 764
DF_CONF_PART = DF_CONFHIT[DF_CONFHIT["id"].isin(only_inter)]
DF_CONF_PART.to_csv("/Users/nquinones/Desktop/764.tsv", sep="\t", index=False)
DF_CONF_PART["id"].value_counts()

# conf_mult 15
only_conf_mult = set(only_conf).intersection(set(MULT_HITS["id"]))
DF_CONF_MULT = DF_CONFHIT[DF_CONFHIT["id"].isin(only_conf_mult)]
DF_CONF_MULT.to_csv("/Users/nquinones/Desktop/15.tsv", sep="\t", index=False)

# mult_annot 283
only_mult_annot = set(MULT_ANNOT["id"]).intersection(set(DF_CONFHIT["id"]))
DF_MULT_ANNOT = DF_CONFHIT[DF_CONFHIT["id"].isin(only_mult_annot)]





(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF01959")])["hit_rfam_acc"].value_counts()
(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF00177")])["hit_rfam_acc"].value_counts()
(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF02540")])["hit_rfam_acc"].value_counts()


CLANS = pd.DataFrame(DF_REAL_CONF["hit_clan_acc"].value_counts())
DF_REAL_CONF[(DF_REAL_CONF.hit_clan_acc == "CL00001")]

DOB_RNAC.to_csv("/Users/nquinones/Desktop/Dob_RNAC.tsv", sep="\t", index=False)
DF_DOUBLEHITS.to_csv("/Users/nquinones/Desktop/part.tsv", sep="\t", index=False)
DF_REAL_CONF.to_csv("/Users/nquinones/Desktop/real.tsv", sep="\t", index=False)