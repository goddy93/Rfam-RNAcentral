#BSUB -J newfam_newfam
#BSUB -o /nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam_nhmmer.job.out
#BSUB -e /nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam_nhmmer.job.err

#PATHS
queryfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam_seq.fasta"
seqdb="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/newfam_seq.fasta"
outfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam_nhmmer.out"
alifile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam_nhmmer.ali"
tblfile="/nfs/production/xfam/users/nataquinones/newfam_nhmmer/out/newfam_nhmmer.tbl"
nhmmer="/nfs/production/xfam/rfam/rfam_rh7/software/bin/nhmmer"

#JOB
$nhmmer -o $outfile -A $alifile --tblout $tblfile --noali --rna --tformat fasta --qformat fasta $queryfile $seqdb