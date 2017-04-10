#Use: /Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/11.goget_cleanali.sh  <ali_name>
# Copies alignment from /clean_alignments into folder in newfams folder
ALI=$1
BASE="${ALI%%.*}"
NEWFOLDER="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/newfams/"$BASE
mkdir $NEWFOLDER
cp /Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/clean_alignments/$ALI $NEWFOLDER
