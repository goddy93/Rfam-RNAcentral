SCRIPT_PATH="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/12.alitool.py"
SCRIPT_PATH2="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/12.b.homehtml.py"
TBL_OUT="/Users/nquinones/Desktop/testdir/TBL_selali.tsv"
ALI_PATH="/Users/nquinones/Desktop/testdir/alis"

touch $TBL_OUT
echo $'file\tname\tnum_seq\talen\tavlen\tlenalen_ratio\tavid\tnum_pub\tnum_db\tcodingwarn\trscapewarn' > $TBL_OUT
cd $ALI_PATH
for folder in *
do  cd $folder
	for file in *.sto
	do cp $file $file.txt
	python $SCRIPT_PATH $file $TBL_OUT
	done
	cd ..
done
cd ..
python $SCRIPT_PATH2 $TBL_OUT $ALI_PATH
