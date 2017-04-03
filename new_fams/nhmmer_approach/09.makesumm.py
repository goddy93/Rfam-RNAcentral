import pandas as pd

TBL_PATH = "/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/05.easelstats.tsv"

df_tbl = pd.read_table(
    TBL_PATH)


ab40 = df_tbl[df_tbl["lenalen_ratio"] > 0.40]

sort = ab40.sort_values(["group", "num_seq", "lenalen_ratio"], ascending=[1, 0, 0])

summary = pd.DataFrame()
for group in set(sort["group"]):
	sub = sort[sort["group"] == group]
	mems = len(sub)
	mean = sub.num_seq.mean()
	maxi = sub.num_seq.max()
	mini = sub.num_seq.min()
	rat = sub.lenalen_ratio.mean()
	line = [[group, mems, mean, maxi, mini, rat]]
	summary = summary.append(line)

summary.columns = ["group", "members" ,"avg_numseq", "max_numseq", "min_numseq", "alenrat"]

summsort = summary.sort_values(["avg_numseq"], ascending=[0])
summsort.to_csv("./summ", sep="\t", index=False)

g_input = 124
sort[sort["group"] == g_input]
