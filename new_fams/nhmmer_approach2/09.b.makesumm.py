import pandas as pd

TBL_PATH = "/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/05.easelstats.tsv"

DF_TBL = pd.read_table(
    TBL_PATH)

SORT = DF_TBL.sort_values(["group", "num_seq", "lenalen_ratio"], ascending=[1, 0, 0])

# SUMMARY
SUMMARY = pd.DataFrame()
for group in set(SORT["group"]):
    sub = SORT[SORT["group"] == group]
    mems = len(sub)
    mean = sub.num_seq.mean()
    maxi = sub.num_seq.max()
    mini = sub.num_seq.min()
    rat = sub.lenalen_ratio.mean()
    line = [[group, mems, mean, maxi, mini, rat]]
    SUMMARY = SUMMARY.append(line)

SUMMARY.columns = ["group", "members", "avg_numseq", "max_numseq", "min_numseq", "alenrat"]
SUMMARY = SUMMARY.set_index(["group"], drop=True)

# SELECTED
SELECTED = SORT
# .. only alignments with less than 40% gaps
SELECTED = SELECTED[SELECTED["lenalen_ratio"] > 0.40]
# .. only alignments with less than 100% id
SELECTED = SELECTED[SELECTED["avid"] < 100]
# .. keep top 3
SELECTED = SELECTED.groupby("group").head(3)
# .. reorder based on lenalen_ratio
SELECTED = SELECTED.sort_values(["group", "lenalen_ratio"], ascending=[1, 0])
# .. keep top one
SELECTED = SELECTED.drop_duplicates(["group"])
# .. index
SELECTED = SELECTED.set_index(["group"], drop=True)

JOIN = pd.concat([SELECTED, SUMMARY], axis=1, join='inner')
JOIN["lenalen_ratio"] = JOIN["lenalen_ratio"].round(2)
JOIN["avg_numseq"] = JOIN["avg_numseq"].round(2)
JOIN["alenrat"] = JOIN["alenrat"].round(2)


SEL_ALI_TBL = JOIN[["file", "num_seq", "alen", "avlen", "lenalen_ratio", "avid"]]
SEL_ALI_TBL.reset_index(level=0, inplace=True)

GRP_TBL = JOIN[["members", "avg_numseq", "max_numseq", "min_numseq", "alenrat", "file"]]
GRP_TBL.reset_index(level=0, inplace=True)

GP_FILE_REL = DF_TBL[["group", "file"]].sort_values(["group"])

SEL_ALI_TBL.to_csv("./TBL_selali.tsv", sep="\t", index=False)
GRP_TBL.to_csv("./TBL_groups.tsv", sep="\t", index=False)
SEL_ALI_TBL["file"].to_csv("./LIST_selali.tsv", sep="\t", index=False)
GP_FILE_REL.to_csv("./TBL_gp-file.tsv", sep="\t", index=False)

# CHECKS
# .. groups that are not in summary
# a = SUMMARY.index.tolist() # all created groups
# b = range(0, len(a)) # all groups with stats
# c = set(b) - set(a)  # things that get dropped because no stats
# d = SELECTED.index.tolist()
# e = set(b) - set(d)  # things that get dropped because avid 100 or below 40 lenalenratio
