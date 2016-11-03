import sys
import pandas as pd

inputfile = sys.argv[1]
outputfile = sys.argv[2]

df = pd.read_table(
	inputfile, 
	skiprows=[0,1], 
	engine="python", 
	sep="\s*|-\n", 
	header=None
	)

df = df[[3,2,1,5,19]] 
df.columns = ['id', 'hit_rfam_acc', 'fam_name', 'hit_clan_acc', 'olp']
df = df.loc[df['olp'] != '=']

df.to_csv(outputfile, sep='\t', index = False)
