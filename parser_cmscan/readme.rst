
Description
===========
Takes Infernal's cmscan table output file and parses it into tab delimited dataframe with only the best scored hits.

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
This parser works under the following conditions:

Table output:
^^^^^^^^^^^^^
Infernal's cmscan table output generated with the following options:
.. code:: bash
	--tblout --fmt 2 --acc --notextw --clanin

Best scored hits:
^^^^^^^^^^^^^^^^^
Parser selects lines from table output where :code:`olp` column is :code:`*` or :code:`ˆ`

In the "olp" column, hits with the “*” do not overlap with any other hits, hits with “ˆ” do overlap with at least one other hit, but none of those overlapping hits have a better score and hits with “=” also overlap with at least one other hit that does have a better score.

Selected columns and renaming:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+--------------+--------------+
| Table output |  Parsed file |
+==============+==============+
| query name   |  id          |
+--------------+--------------+
| accession    | hit_rfam_acc |
+--------------+--------------+
| target name  | fam_name     |
+--------------+--------------+
| clan name    | hit_clan_acc |
+--------------+--------------+
| opl          | opl          |
+--------------+------------ -+

Tweaking these options:
^^^^^^^^^^^^^^^^^^^^^^^
Parser should work with alternative options by modifying lines 15-17 from :code:`parser_cmscan.py`
