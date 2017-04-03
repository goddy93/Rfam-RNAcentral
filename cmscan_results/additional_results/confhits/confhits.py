import pandas as pd
import numpy as np

IN_SAMEHIT = "./query_files/query_samehit"
IN_CONFHIT = "./query_files/query_confhit"


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

SAMEHIT_L = DF_SAMEHIT["id"].tolist()
CONFHIT_L = DF_CONFHIT["id"].tolist()

DOUBLE_HITS_SET = set(SAMEHIT_L).intersection(set(CONFHIT_L))
DOUBLE_HITS_L = list(DOUBLE_HITS_SET)
REAL_CONF_SET = set(CONFHIT_L)-set(DOUBLE_HITS_L)
REAL_CONF_L = list(REAL_CONF_SET)


DF_DOUBLEHITS = DF_CONFHIT[DF_CONFHIT["id"].isin(DOUBLE_HITS_L)]
DF_REAL_CONF = DF_CONFHIT[DF_CONFHIT["id"].isin(REAL_CONF_L)]

ANNOT = pd.DataFrame(DF_REAL_CONF["rfam_acc"].value_counts())

(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF01960")])["hit_rfam_acc"].value_counts()
(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF01959")])["hit_rfam_acc"].value_counts()
(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF00177")])["hit_rfam_acc"].value_counts()
(DF_REAL_CONF[(DF_REAL_CONF.rfam_acc == "RF02540")])["hit_rfam_acc"].value_counts()


CLANS = pd.DataFrame(DF_REAL_CONF["hit_clan_acc"].value_counts())
DF_REAL_CONF[(DF_REAL_CONF.hit_clan_acc == "CL00001")]



