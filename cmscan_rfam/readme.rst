Description
===========
Script and options for submitting **INFERNAL 1.1.2 cmscan** job to cluster with specific options.

``cmscan`` options
===================

.. code:: bash

	cmscan --tblout [tblout_path] -Z 12063.99847 --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin [clanin_path] [cm_path] [input_path]

For details check `INFERNAL User guide <http://eddylab.org/infernal/Userguide.pdf>`_

Z option
--------
The selected Z parameter is 12063.99847 Mb, obtained through the following process:

Run the ``esl-seqstat`` tool from Infernal:

.. code:: bash

	/path_to_infernal/infernal-1.1.1/easel/miniapps/esl-seqstat [file_of_interest]

Output looks like this:

.. code::

	Format:              FASTA
	Alphabet type:       RNA
	Number of sequences: 9386112
	Total # residues:    6031999237
	Smallest:            10
	Largest:             244296
	Average length:      642.7

To obtain Mb 
<<<<<<< HEAD
..code:: bash
	Number of residues * 2 / 1000000 
=======

.. code:: bash

	Number of residues * 2 / 1000000 

Which in this case = ``12063.99847``


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

	#BSUB -J cmscan_1
	#BSUB -o /nfs/gns/homes/nataquinones/cmscan/job_out/cmscan_1.txt

	#PATHS
	input_path="/nfs/gns/homes/nataquinones/fasta_slicer/files/rnacentral.fastagroup_1.fasta"
	tblout_path="/nfs/gns/homes/nataquinones/cmscan/tables/cmscan_tbl_1.txt"

Submit job:

.. code:: bash

	bsub < cmscan_rfam_sample.sh 


Long job submission
===================
Alternatively, the whole options can be specified after ``bsub``:

.. code:: bash

	bsub -q mpi-rh7 -J [job_name] -o [job_output] -M 10000 -R "rusage[mem=10000]" -n 4 -R span[hosts=1] -a openmpi mpiexec -mca btl ^openib -np 4 /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan --tblout [tblout_file.txt] -Z 12063.99847 --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin /nfs/gns/homes/nataquinones/RfamCM/Rfam.cm [input_file.fasta]


Example
-------
For:

.. code:: bash

	job_name = cmscan_1
	job_output = /nfs/gns/homes/nataquinones/cmscan/job_out/cmscan_1.txt
	tblout_file.txt = /nfs/gns/homes/nataquinones/cmscan/tables/cmscan_tbl_1.txt
	input_file.fasta = /nfs/gns/homes/nataquinones/fasta_slicer/files/rnacentral.fastagroup_1.fasta

Submission would be:

.. code:: bash

	bsub -q mpi-rh7 -J cmscan_1 -o /nfs/gns/homes/nataquinones/cmscan/job_out/cmscan_1.txt -M 10000 -R "rusage[mem=10000]" -n 4 -R span[hosts=1] -a openmpi mpiexec -mca btl ^openib -np 4 /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/src/cmscan --tblout /nfs/gns/homes/nataquinones/cmscan/tables/cmscan_tbl_1.txt -Z 12064 --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin /nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin /nfs/gns/homes/nataquinones/RfamCM/Rfam.cm /nfs/gns/homes/nataquinones/fasta_slicer/files/rnacentral.fastagroup_1.fasta

