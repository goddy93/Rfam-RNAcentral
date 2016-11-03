Cluster options
===============
..code::
	username@ebi-005.ebi.ac.uk
	module load mpi/openmpi-x86_64


Job submission script
==========================
..code::

	bsub < cmscan_rfam.sh 

What's on `cmscan_rfam.sh`
------------------------
The job submission script with the right options.
The following things should be specified for it to work:

..code::
	#BSUB -J [job_name]
	#BSUB -o [path/jobouput.txt]

	#PATHS
	input_path="path/input.fasta"
	tblout_path="path/tblout.txt"

Example
-------
..code::
	bsub < cmscan_rfam_sample.sh 

Where:
..code::
	#BSUB -J jobname
	#BSUB -o /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/cmscan_out.txt

	#PATHS
	input_path="/nfs/gns/homes/nataquinones/slice_RNAcentral/small_slices/rnacentral_active_1.1.fasta"
	tblout_path="/nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/cmscan.tblout_1.1.txt"


Long job submission
======================================
..code::
bsub -q mpi-rh7 -J [job_name] -o [job_output] -M 10000 -R "rusage[mem=10000]" -n 4 -R span[hosts=1] -a openmpi mpiexec -mca btl ^openib -np 4 /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan --tblout [tblout_file.txt] --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin /nfs/gns/homes/nataquinones/RfamCM/Rfam.cm [input_file.fasta]

Example
-------
For:
..code::
	job_name = test
	job_output = /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/test.txt
	tblout_file.txt = /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/tblout_test.txt
	input_file.fasta = /nfs/gns/homes/nataquinones/slice_RNAcentral/small_slices/rnacentral_active_1.1.fasta

Submission would be:
	bsub -q mpi-rh7 -J test -o /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/test.txt -M 10000 -R "rusage[mem=10000]" -n 4 -R span[hosts=1] -a openmpi mpiexec -mca btl ^openib -np 4 /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan --tblout /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/tblout_test.txt --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin /nfs/gns/homes/nataquinones/RfamCM/Rfam.cm /nfs/gns/homes/nataquinones/slice_RNAcentral/small_slices/rnacentral_active_1.1.fasta
