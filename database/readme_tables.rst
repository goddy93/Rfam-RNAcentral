readme_tables
========================
+-------------------+---------------------------------------------------------------------------------+
| ``cmscan_hits``   |    Contains information of the output cmscan tables                             |
+-------------------+---------------------------------------------------------------------------------+
| ``cmscan_run``    |    Contains all the URSs from the file                                          |
+-------------------+---------------------------------------------------------------------------------+
|``id_mapping``     |   Contains the linked databases to each URS, including the ``rna_type``         |
+-------------------+---------------------------------------------------------------------------------+
|``taxonomy``       |   Contains ncbi tax id                                                          |
+-------------------+---------------------------------------------------------------------------------+
|``urs_condensed``  |  Uses ``id_mapping`` table and concats fields to make "group queries" easier    |
+-------------------+---------------------------------------------------------------------------------+
|``urs_rnacentral`` | Contains all the URSs and the length of the related sequence                    |
+-------------------+---------------------------------------------------------------------------------+

Table ``urs_rnacentral``
------------------------
Table generated from output of `fasta_tools/fasta_seq-len.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/fasta_tools/fasta_seq-len.py>`_. when running it for file ``rnacentral_nhmmer.fasta``.

.. code:: SQL

	CREATE TABLE urs_rnacentral(
		id VARCHAR(13),
		len VARCHAR(6),
		PRIMARY KEY (id)
		);

	LOAD DATA LOCAL INFILE "path/to/file_seq-len.txt" INTO TABLE length IGNORE 1 LINES;

	ALTER TABLE urs_rnacentral
		CHANGE COLUMN len len
		INT(6);

Resulting number of rows: 9386112

Table ``taxonomy``
-----------------
Table generated from a selection of the ``taxonomy`` table in `Rfam public database <http://rfam.github.io/docs/>`_.

Saved query as ``taxonomy.txt``:

.. code:: SQL

	SELECT t.ncbi_id, t.species, t.tax_string
	FROM taxonomy t
		
Table:

.. code:: SQL

	CREATE TABLE taxonomy (
		ncbi_id VARCHAR(10),
		species VARCHAR(100),
		tax_string VARCHAR(100),
		PRIMARY KEY (ncbi_id)
	);

	LOAD DATA LOCAL INFILE "path/to/taxonomy.txt" INTO TABLE taxonomy IGNORE 1 LINES;

Table ``id_mapping``
--------------------
Table generated from the file ``id_mapping`` file in the `RNAcentral FTP site <http://rnacentral.org/downloads>`_

.. code:: SQL

	CREATE TABLE id_mapping (
		id VARCHAR(13),
		db VARCHAR(10),
		db_acc VARCHAR(50),
		tax_id VARCHAR(10),
		rna_type VARCHAR(10)
	);

	LOAD DATA LOCAL INFILE "path/to/id_mapping.txt" INTO TABLE id_mapping;

	ALTER TABLE id_mapping
	ADD FOREIGN KEY (id) REFERENCES urs_rnacentral (id);
	
	--Not working*
	ALTER TABLE id_mapping
	ADD FOREIGN KEY (tax_id) REFERENCES taxonomy (ncbi_id);


Table ``cmscan_hits``
---------------------
Table to input files from cmscan process

.. code:: SQL

	CREATE TABLE cmscan_hits (
		id VARCHAR(13),
		hit_rfam_acc VARCHAR(7),
		fam_name VARCHAR(30),
		hit_clan_acc VARCHAR(7),
		olp VARCHAR(1),
		e_value VARCHAR(10),
		FOREIGN KEY (id)
			REFERENCES urs_rnacentral (id)
	);

This table is loaded with the output from `parser_cmscan.py <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/parser_cmscan>`_ To load the table use `load_tbl.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/database/load_tbl.py>`_ in a directory with **all and only** the files you want to upload. As follows:

.. code:: Bash

	cd /path/to/dir/parsed_tables/
	python load_tbl.py


Table ``cmscan_run``
---------------------
Table to keep track of URSs that have already been scanned. It is generated from output of `fasta_id.py <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/fasta_tools>`_. 

.. code:: SQL

	CREATE TABLE cmscan_run (
		id VARCHAR(13) NOT NULL,
		file VARCHAR(20),
		PRIMARY KEY(id)
	);

This table is loaded with the output from `fasta_tools/fasta_id.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/fasta_tools/fasta_id.py>`_ To load the table use `load_id.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/database/load_id.py>`_ in a directory with **all and only** the files you want to upload. As follows:

.. code:: Bash

	cd /path/to/dir/ids/
	python load_id.py

Table ``urs_condensed``
-----------------------
Uses ``id_mapping`` table and collapses certain fields to make queries easier.

.. code:: SQL

	CREATE TABLE urs_condensed
	SELECT
		im.id,
		GROUP_CONCAT(DISTINCT im.db) AS db,
		GROUP_CONCAT(DISTINCT IF(im.db LIKE '%RFAM%',im.db_acc,NULL)) AS rfam_acc,
		GROUP_CONCAT(DISTINCT im.rna_type) AS rna_type,
		GROUP_CONCAT(DISTINCT im.tax_id) AS tax_id
	FROM id_mapping im
	GROUP BY im.id;

	ALTER TABLE urs_condensed
	ADD PRIMARY KEY (id);

The concatenated ``tax_id`` field can get very large, this was needed before creating the table:

.. code:: SQL

	SET group_concat_max_len=100000


