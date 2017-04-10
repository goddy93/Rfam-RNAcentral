#BSUB -J 03.c
#BSUB -o /nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.job.job
#BSUB -e /nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.job.err

# ----PATHS select_ali----------
TBL_PATH="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/03.b.rmsingle.tbl"
BESTMARK_OUT="/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/03.c.bestmark.tbl"

#JOB
source /nfs/production/xfam/users/nataquinones/nhmmer_families/venv-nhmmer_families/bin/activate
python /Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/03.c.bestmark.py $TBL_PATH $BESTMARK_OUT