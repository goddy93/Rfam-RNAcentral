
Description
===========
Takes **INFERNAL 1.1.2 cmscan** table output file and parses it into tab delimited dataframe with only the best scored hits.

Use
====

.. code:: bash

	#create a new virtual environment
	virtualenv /project_path/venv-parser

	#activate virtual environment
	source /project_path/venv-parser/bin/activate

	#install Python dependencies
	cd /project_path/parser_cmscan
	pip install -r requirements.txt

	#run python script
	python parser_cmscan.py [input_tblout] [output_file]

Example
========

.. code:: bash

  python parser_cmscan.py ./sample_files/tblout_sample.txt ./sample_files/par.tblout_sample.txt	

Specifics
=========

Table output:
^^^^^^^^^^^^^
Parser works with an **Infernal's cmscan** table output generated with the following options:

.. code:: bash

	--tblout --fmt 2 --acc --notextw --clanin

Choses best scored hits:
^^^^^^^^^^^^^^^^^^^^^^^^
Parser selects lines from table output where :code:`olp` column from the table output is :code:`*` or :code:`ˆ`

	In the "olp" column:
	
	- Hits with the “*” do not overlap with any other hits.
	
	- Hits with “ˆ” do overlap with at least one other hit, but none of those overlapping hits have a better score.
	
	- Hits with “=” also overlap with at least one other hit that does have a better score. 
	
	(see `INFERNAL User's Guide <http://eddylab.org/infernal/Userguide.pdf>`_)

Selected columns and renaming:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-----------------------+--------------+
| Infernal table output |  Parsed file |
+=======================+==============+
| query name            |  id          |
+-----------------------+--------------+
| accession             | hit_rfam_acc |
+-----------------------+--------------+
| target name           | fam_name     |
+-----------------------+--------------+
| clan name             | hit_clan_acc |
+-----------------------+--------------+
| opl                   | opl          |
+-----------------------+--------------+

Tweaking these options:
^^^^^^^^^^^^^^^^^^^^^^^
Parser should work with alternative options by modifying :code:`lines 15-17` from :code:`parser_cmscan.py`
