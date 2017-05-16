import sys
import pandas as pd

inputfile = sys.argv[1]
outputfile = sys.argv[2]

df = pd.read_table(
	inputfile, 
	comment="#", 
	engine="python", 
	sep="\s*|-\n", 
	header=None,
	usecols=range(20)
	)

df = df[[3,2,1,5,19, 17]] 
df.columns = ['id', 'hit_rfam_acc', 'fam_name', 'hit_clan_acc', 'olp', 'e_value']
df = df.loc[df['olp'] != '=']

df.to_csv(outputfile, sep='\t', index = False)
