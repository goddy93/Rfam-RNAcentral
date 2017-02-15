#BSUB -J newfam-newfam
#BSUB -o /nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam-nhmmer.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam-nhmmer.job.err

#PATHS
queryfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam_seq.fasta"
seqdb="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam_seq.fasta"
outfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam-nhmmer.out"
alifile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam-nhmmer.ali"
tblfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam-nhmmer.tbl"
dtblfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam-nhmmer.dtbl"
nhmmer="/nfs/production/xfam/rfam/rfam_rh7/software/bin/nhmmer"

#JOB
$nhmmer -o $outfile -A $alifile --tblout $tblfile --dfamtblout $dtblfile --noali --rna --tformat fasta --qformat fasta $queryfile $seqdb