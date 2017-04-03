#Use: /Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/13.coding_check.sh  <sto file>

ALI=$1

# Convert stockholm file to clustal
BASE="${ALI%%.sto}"
/Users/nquinones/Documents/infernal-1.1.2/easel/miniapps/esl-reformat --replace .:- --informat stockholm  -d -o $BASE.aln clustal $ALI

# Run RNAcode with clustal format output
ALIW=$BASE.aln
OUT="$BASE.rnacode.out"

RNAcode --eps-dir rnacode_eps --outfile $OUT --eps $ALIW
