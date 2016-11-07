Rfam-RNAcentral Database
========================
Database design
---------------

Table creation
--------------

Table ``rnacentral_map``
^^^^^^^^^^^^^^^^^^^^^^^
.. code :: MySQL

	CREATE TABLE rnacentral_map
	SELECT 
		im.id, 
		GROUP_CONCAT(DISTINCT im.db) AS db,
		GROUP_CONCAT(DISTINCT IF(im.db LIKE '%RFAM%',im.db_acc,NULL)) AS rfam_acc,
		GROUP_CONCAT(DISTINCT im.rna_type) AS rna_type
	FROM id_mapping im
	GROUP BY im.id

Make id primary key:

.. code :: MySQL

	ALTER TABLE rnacentral_map
	ADD PRIMARY KEY (id);

Table ``cmscan_hits``
^^^^^^^^^^^^^^^^^^^^^^^
.. code :: MySQL

	CREATE TABLE cmscan_hits
	(id VARCHAR(13),
	hit_rfam VARCHAR(7),
	fam_name VARCHAR(30),
	hit_clan_acc VARCHAR(7),
	olp VARCHAR(1),
	e_value VARCHAR(10)
	);

Make forgein key:

.. code :: MySQL

	ALTER TABLE cmscan_hits
	ADD FOREIGN KEY (id)
	REFERENCES rnacentral_map (id);

Load files into table:

.. code :: MySQL

	LOAD DATA LOCAL INFILE "file_to_be_loaded.txt" INTO TABLE cmscan_hits IGNORE 1 LINES;

Loaded file should be in the output format of `parser_cmscan <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/parser_cmscan>`_ to 

Group queries
--------------
GROUP *SAME HIT*: In Rfam, same hit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: MySQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NOT NULL -- in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- got hit
	AND rm.rfam_acc = ch.hit_rfam_acc -- same

GROUP *CONFLICTING HIT*: In Rfam, different hit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: MySQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NOT NULL -- in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- got hit
	AND rm.rfam_acc != ch.hit_rfam_acc -- different

#MULTIPLE HITS FILTER
SELECT
	ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families
FROM cmscan_hits ch 
GROUP BY ch.id

GROUP *LOST IN SCAN*: In Rfam, got no hits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: MySQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NOT NULL -- in Rfam
	AND ch.hit_rfam_acc IS NULL -- no hit

GROUP *NEW MEMBERS*: Not in Rfam, got hit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: MySQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NULL -- not in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- got hit

GROUP *NEW FAMILY*: Not in Rfam, no hits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code :: MySQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NULL -- not in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- no hit


