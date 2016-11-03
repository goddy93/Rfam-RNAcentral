Description
===========
Script and options for submitting **Infernal's cmscan** job to LSF cluster.

Cluster login
=============

.. code:: bash

	username@ebi-005.ebi.ac.uk
	module load mpi/openmpi-x86_64


Job submission script
=====================

What's in ``cmscan_rfam.sh`` ?
----------------------------
The job submission script with specific ``bsub`` and the ``cmscan`` options.

How to use
----------
Paths/files in the following lines should be specified:

.. code:: bash

	#BSUB -J [job_name]
	#BSUB -o [path/jobouput.txt]

	#PATHS
	input_path="path/input.fasta"
	tblout_path="path/tblout.txt"

Submission
----------

.. code:: bash

	bsub < cmscan_rfam.sh 

Example
-------
Change the following lines and save as ``cmscan_rfam_sample.sh``:

.. code:: bash

	#BSUB -J jobname
	#BSUB -o /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/cmscan_out.txt

	#PATHS
	input_path="/nfs/gns/homes/nataquinones/slice_RNAcentral/small_slices/rnacentral_active_1.1.fasta"
	tblout_path="/nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/cmscan.tblout_1.1.txt"

Submit job:

.. code:: bash

	bsub < cmscan_rfam_sample.sh 


Long job submission
===================
Alternatively, the whole options can be specified after ``bsub``:

.. code:: bash

	bsub -q mpi-rh7 -J [job_name] -o [job_output] -M 10000 -R "rusage[mem=10000]" -n 4 -R span[hosts=1] -a openmpi mpiexec -mca btl ^openib -np 4 /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan --tblout [tblout_file.txt] --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin /nfs/gns/homes/nataquinones/RfamCM/Rfam.cm [input_file.fasta]


Example
-------
For:

.. code:: bash

	job_name = jobname
	job_output = /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/test.txt
	tblout_file.txt = /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/tblout_test.txt
	input_file.fasta = /nfs/gns/homes/nataquinones/slice_RNAcentral/small_slices/rnacentral_active_1.1.fasta

Submission would be:

.. code:: bash

	bsub -q mpi-rh7 -J jobname -o /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/test.txt -M 10000 -R "rusage[mem=10000]" -n 4 -R span[hosts=1] -a openmpi mpiexec -mca btl ^openib -np 4 /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan --tblout /nfs/gns/homes/nataquinones/RNAcentral_cmscan/prueba/tblout_test.txt --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin /nfs/gns/homes/nataquinones/RfamCM/Rfam.cm /nfs/gns/homes/nataquinones/slice_RNAcentral/small_slices/rnacentral_active_1.1.fasta
