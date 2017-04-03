#BSUB -J 03.b
#BSUB -o /nfs/production/xfam/users/nataquinones/nhmmer_families/03.a/03.b.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/nhmmer_families/03.a/03.b.job.err

# ----PATHS select_ali----------
TBL_PATH="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/test100.tbl"
PAR_TBL_OUT="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/03.a.parsed.tbl"

#JOB
source /nfs/production/xfam/users/nataquinones/nhmmer_families/venv-nhmmer_families/bin/activate
python /Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/03.a.parse.py $TBL_PATH $PAR_TBL_OUT