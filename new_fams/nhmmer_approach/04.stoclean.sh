#BSUB -J 04
#BSUB -o /nfs/production/xfam/users/nataquinones/nhmmer_families/new/04.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/nhmmer_families/new/04.job.err

# ----PATHS select_ali----------
TBL_PATH = "/nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.c.bestmark.tbl"
ALI_PATH = "/nfs/production/xfam/users/nataquinones/nhmmer_families/alignments/"
SEL_ALI_PATH = "/nfs/production/xfam/users/nataquinones/nhmmer_families/clean_alignments/"

#JOB
source /nfs/production/xfam/users/nataquinones/nhmmer_families/venv-nhmmer_families/bin/activate
python /nfs/production/xfam/users/nataquinones/nhmmer_families/new/04.stoclean.py $TBL_PATH $ALI_PATH $SEL_ALI_PATH