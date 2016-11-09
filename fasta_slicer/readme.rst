Description
===========
Slices FASTA file given the number of elements to be saverd per file.

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
  
Extras
===========
```fasta_len.py`` is a small script which reads a ``FASTA`` file and outputs two columns with the *accession number* and its corresponding *length* 
