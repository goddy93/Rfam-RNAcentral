#BSUB -J 03.c
#BSUB -o /nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.job.err

# ----PATHS select_ali----------
TBL_PATH="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.b.single.par.tbl"
BESTMARK_OUT="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.bestmark.tsv"

#JOB
source /nfs/production/xfam/users/nataquinones/nhmmer_families/venv-nhmmer_families/bin/activate
python /nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.bestmark.py $TBL_PATH $BESTMARK_OUT