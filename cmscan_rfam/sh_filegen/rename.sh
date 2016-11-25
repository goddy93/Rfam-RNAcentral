#RENAME
for file in *.fasta
	do mv $file ${file//rnacentral.fastagroup/cms_rnac}
	done



