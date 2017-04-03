#BSUB -J 05
#BSUB -o /nfs/production/xfam/users/nataquinones/nhmmer_families/new/05.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/nhmmer_families/new/05.job.err

# ----PATHS select_ali----------
ALISTAT_PATH="/nfs/production/xfam/rfam/rfam_rh7/software/bin/esl-alistat"
ALI_PATH="/nfs/production/xfam/users/nataquinones/nhmmer_families/clean_alignments/"
ALISTATS_TBL="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/05.easelstats.tsv"
COMP_LIST="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/07.components.list"

#JOB
source /nfs/production/xfam/users/nataquinones/nhmmer_families/venv-nhmmer_families/bin/activate
python /nfs/production/xfam/users/nataquinones/nhmmer_families/new/05.easelstats.py $ALISTAT_PATH $ALI_PATH $ALISTATS_TBL $COMP_LIST