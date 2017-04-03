#BSUB -J 07
#BSUB -M 30000
#BSUB -R "rusage[mem=30000]"
#BSUB -o /nfs/production/xfam/users/nataquinones/nhmmer_families/new/07.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/nhmmer_families/new/07.job.err

# ----PATHS select_ali----------
TBL_PATH="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/03.b.single.par.tbl"
COMPONENTS_OUT="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/07.components.list"
CLIQUES_OUT="/nfs/production/xfam/users/nataquinones/nhmmer_families/new/07.cliques.list"

#JOB
source /nfs/production/xfam/users/nataquinones/nhmmer_families/venv-nhmmer_families/bin/activate
python /nfs/production/xfam/users/nataquinones/nhmmer_families/new/07.nxgroups.py $TBL_PATH $COMPONENTS_OUT $CLIQUES_OUT