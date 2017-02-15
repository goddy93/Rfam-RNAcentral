#BSUB -q mpi-rh7
#BSUB -J clus3
#BSUB -o /nfs/research2/nobackup/nqo/cluster_newfam/cluster3/cluster3.out
#BSUB -e /nfs/research2/nobackup/nqo/cluster_newfam/cluster3/cluster3.err
#BSUB -M 10000
#BSUB -n 4

#JOB
/nfs/nobackup/ensemblgenomes/apetrov/nhmmer/cd-hit-est \
        -i /nfs/research2/nobackup/nqo/cluster_newfam/eunewfam.fasta \
        -o /nfs/research2/nobackup/nqo/cluster_newfam/cluster3/eunewfam-clustered3.fasta \
        -G 0 \
        -M 0 \
        -n 8 \
        -aS 0.4 \
        -aL 0.4 \
        -s 0.6 \
        -g 1 \
        -r 1 \
        -T 0 \
        -B 1
