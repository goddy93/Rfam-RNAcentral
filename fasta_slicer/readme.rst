Description
===========
Slices FASTA file given the number of elements to be saverd per file.
(Small modifications from code: `http://biopython.org/wiki/Split_large_file <http://biopython.org/wiki/Split_large_file>`_ )

Use
====
.. code:: bash

	#create a new virtual environment
	virtualenv /project_path/venv-slicer

	#activate virtual environment
	source /project_path/venv-slicer/bin/activate

	#install Python dependencies
	cd /project_path/fasta_slicer
	pip install -r requirements.txt

	#run python script
	python slicer.py [num_records] [input_fasta]

Example
========

.. code:: bash

  python slicer.py 10 ./sample_files/example.txt	