Description
===========
``fasta_slicer.py``
-------------------
Slices ``FASTA`` file given the number of elements to be saverd per file.


(Small modifications this code: `http://biopython.org/wiki/Split_large_file <http://biopython.org/wiki/Split_large_file>`_ )


Use
====
.. code:: bash

	#create a new virtual environment
	virtualenv /project_path/venv-fasta_slicer

	#activate virtual environment
	source /project_path/venv-fasta_slicer/bin/activate

	#install Python dependencies
	cd /project_path/fasta_slicer
	pip install -r requirements.txt

	#run python script
	python fasta_slicer.py [num_records] [input_fasta]


Example
========
Input

.. code:: bash

  python fasta_slicer.py 2 ./sample_files/example.fasta

Output

.. code:: bash

  Wrote 2 records to sample_files/example.fastagroup_1.fasta
  Wrote 2 records to sample_files/example.fastagroup_2.fasta
  Wrote 1 records to sample_files/example.fastagroup_3.fasta
  

Other minor tools
=================
``fasta_seq_len.py``
--------------------
Produces a tab delimited file with the sequence id, length for each record in the ``FASTA`` file. 

``fasta_id.py``
---------------
Produces a file with a list of the sequence id for each record in the ``FASTA`` file. 

USE
^^^^
Both use the same requirements as ``fasta_silcer.py`` and can be used as follows:

.. code:: bash

	python fasta_seq_len.py [input_fasta]

	python fasta_id.py [input_fasta]
