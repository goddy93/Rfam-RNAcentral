import sys
import os
import pandas as pd
import pickle

ALISTAT_PATH = sys.argv[1]
ALI_PATH = sys.argv[2]
ALISTATS_TBL = sys.argv[3]
COMP_LIST = sys.argv[4]

with open(COMP_LIST, 'rb') as f:
    comp = pickle.load(f)

info_table = pd.DataFrame()
info_table["file"] = os.listdir(ALI_PATH)
info_table["name"] = info_table["file"].str.replace(r"[.].*", "")
for i in range(0, len(info_table)):
    ex_string = "%s --rna %s%s" % (ALISTAT_PATH, ALI_PATH, info_table["file"][i])
    b = os.popen(ex_string).readlines()
    values = []
    for line in b:
        values.append(line.split()[-1])
    num_seq = int(values[2])
    alen = int(values[3])
    diff = int(values[6]) - float(values[5])
    avlen = float(values[7])
    lenalen_ratio = avlen / alen
    avid = int(values[8].strip("%"))
    info_table.set_value(i, "num_seq", num_seq)
    info_table.set_value(i, "alen", alen)
    info_table.set_value(i, "diff", diff)
    info_table.set_value(i, "avlen", avlen)
    info_table.set_value(i, "lenalen_ratio", lenalen_ratio)
    info_table.set_value(i, "avid", avid)

for i in range(0, len(info_table)):
    for sublist in comp:
        if info_table["name"][i] in sublist:
            info_table.set_value(i, "group", comp.index(sublist))

info_table["num_seq"] = info_table["num_seq"].astype(int)
info_table["alen"] = info_table["alen"].astype(int)
info_table["diff"] = info_table["diff"].astype(int)
info_table["group"] = info_table["group"].astype(int)

info_table = info_table[["group", "name", "num_seq", "alen", "diff", "avlen", "lenalen_ratio", "avid", "file"]]
info_table = info_table.sort_values(["num_seq", "lenalen_ratio"], ascending=[0, 0])

info_table.to_csv(ALISTATS_TBL, sep='\t', index=False)
