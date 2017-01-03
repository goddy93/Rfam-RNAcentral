Rfam-RNAcentral
===============
Contents
********
`cmscan_results <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/cmscan_results>`_
  Uses ``database`` to generate plots. Includes script to generate pie chart showing the URSs belonging to each group (see database), two "rna_type" cleaners to generate "rna_type" bars with members per group.

`cmscan_rfam <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/cmscan_rfam>`_
  Script and options for submitting *INFERNAL cmscan* job to cluster with specific options, cheat sheets, ``.sh`` file generator, etc.

`database <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/database>`_
  *Readme* information about the database construction and python scripts for loading tables.

`fasta_slicer <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/fasta_slicer>`_
  Slices ``FASTA`` file, given the number of elements to be saved per file. Other minor tools for FASTA files included.

`new_fams <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/new_fams>`_
  (Nothing yet)

`parser_cmscan <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/parser_cmscan>`_
  Takes *INFERNAL cmscan* table output file and parses it into tab delimited dataframe with the best scored hits.

Project objective
*****************
Characterize the relationship between *Rfam* and *RNAcentral* databases by scanning RNAcentral with the Rfam covariance model. This allows to explore the overlap (in terms of rna_type, database of origin, etc.), review inconsistencies, assess sequence coverage and search for potential new families.

Workflow
*********
1. Scan (`cmscan_results <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/cmscan_results>`_)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1.1 Slice big FASTA file with all RNAcentral URSs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Slice ``rnacentral_nhmmer.fasta`` with `fasta_tools/fasta_slicer.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/fasta_tools/fasta_slicer.py>`_ (`readme/use <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/fasta_tools>`_)

  The file is too large for it to be ``cmscan``-ned in a single job, so it was sliced into 470 files. The ``rnacentral_nhmmer.fasta`` file should be used to avoid problems with some of the *Infernal* and *Easel* tools.

1.2 Rename slices
~~~~~~~~~~~~~~~~~
Rename slices with `cmscan_rfam/rename.sh <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_rfam/rename.sh>`_

  This renames them into ``cms_rnac_{i}.fasta`` for each *i* slice to have an easier name file to handle (which will also be used in the output and job submission). (This should be integrated into the ``fasta_slicer.py`` and this section removed.) 

1.3 Generate ``.sh`` files for job submission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The files can be generated with a script like `cmscan_rfam/shfile_generator.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_rfam/sh_filegen/shfile_generator.py>`_ (`readme <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_rfam/readme.rst>`_  with detailed ``cmscan`` options.)
A generic ``.sh`` file looks like `/cmscan_rfam/cmscan_rfam.sh <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_rfam/cmscan_rfam.sh>`_ 

1.4 Submit jobs
~~~~~~~~~~~~~~~
All the ``.sh`` files are placed in the same directory and were submited in a group:

.. code:: bash

  for file in ./*.sh
    do
    bsub -g /rnacrfam < $file
  done

2. Build database
^^^^^^^^^^^^^^^^^	
2.1 Parse cmscan tables (`parser_cmscan <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/parser_cmscan>`_)
~~~~~~~~~~~~~~~~~~~~~~~~
The ``.tbl`` files are parsed with `parser_cmscan.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/parser_cmscan/parser_cmscan.py>`_ to generate the files that are then loaded into the database.

2.2 Make and load tables (`database <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/database>`_)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The database consists of 6 tables that are created and loaded as specified in `database <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/database>`_ 

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

3. Summary results
^^^^^^^^^^^^^^^^^^^	
3.1 Groups
~~~~~~~~~~
The ``MySQL`` queries to filter them are described in `readme_queries.rst <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/readme_queries.rst>`_ The groups are defined as:

+----------------------------------------------------------+----------------------------------+
| Rfam                                                     | No Rfam                          |
+---------------------------------------+------------------+-----------------+----------------+
| Hits                                  | No hits          | Hits            | No hits        |
+-----------------+---------------------+                  |                 |                |
| Same            | Not-same            |                  |                 |                |
+-----------------+---------------------+------------------+-----------------+----------------+
| **SAME HIT**    | **CONFLICTING HIT** | **LOST IN SCAN** | **NEW MEMBERS** | **NEW FAMILY** |
+-----------------+---------------------+------------------+-----------------+----------------+

3.2 Extract information from queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The *group queries* for each group are saved as tab delimited tables, through something like:

.. code:: SQL

  SELECT *
  FROM *
  WHERE *
  INTO OUTFILE [file_name]
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY ""
  ESCAPED BY ""
  LINES TERMINATED BY '\n';

Names of the files and specific queries can be found in `cmscan_results/queries_astables <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/queries_astables.rst>`_

3.3 rna_type cleanup
~~~~~~~~~~~~~~~~~~~~
The ``rna_type`` annotation tends to be inconsistent across databases. Since a unique ``rna_type`` is assigned for each URS by concatenating the different strings (see `database/readme_tables:Table urs_condensed <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/database/readme_tables.rst>`_) this causes a cluttered set of rna types that are redundant or contradicting.

To clean-up the ``rna_type`` there are two scripts with dictonaries that substitute each type:

a. `00.rnatype_cleanup.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/00.rnatype_cleanup.py>`_ (does it strictly, doesn't combine groups like ``xRNA`` with ``xRNA,other``) 

b. `00.rnatype_cleanup_lato.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/00.rnatype_cleanup_lato.py>`_ (does it broadly, merges groups like ``xRNA`` and ``xRNA,other``

3.4 Plots
~~~~~~~~~~
- `01.pie_global.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/01.pie_global.py>`_ : Pie chart with the count of all the URS assigned to each *group* (Same hit, Conflicting hit, Lost in scan, New members and New families) 

- `02.bar_rnatype.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/02.bar_rnatype.py>`_ : Bar chart that separates ``rna_types`` per *group*.

- `03.bars_relevance.py <https://github.com/nataquinones/Rfam-RNAcentral/blob/master/cmscan_results/03.bars_relevance.py>`_ : Produces several bar plots of relevance measures. Separates ``rna_types`` into "want in Rfam" and "don't want in Rfam" groups.

      *An alternative for steps 3.3 and 3.4 is quering directly in the python script, using ``sqlalchemy``. This is useful if the database is to be updated constantly, but proved to be very slow and very inefficient process if the plots are generated trough separate scripts. An example of how this could work is shown in `sqlalch_plots<https://github.com/nataquinones/Rfam-RNAcentral/tree/master/cmscan_results/sqlalch_plots>`_
