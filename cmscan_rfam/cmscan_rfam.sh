#BSUB -q mpi-rh7
#BSUB -J [job_name]
#BSUB -o [path/jobouput.txt]
#BSUB -M 10000
#BSUB -R "rusage[mem=10000]"
#BSUB -n 4
#BSUB -R span[hosts=1]
#BSUB -a openmpi mpiexec
#BSUB -mca btl ^openib
#BSUB -np 4

#PATHS
input_path="path/input.fasta"
tblout_path="path/tblout.txt"
cmscan="/nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan"
clanin_path="/nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin"
cm_path="/nfs/gns/homes/nataquinones/RfamCM/Rfam.cm"

#JOB
$cmscan --tblout $tblout_path --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin $clanin_path $cm_path $input_path