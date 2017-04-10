autoRfam README
===============

Workflow
********
0. Get sequences
~~~~~~~~~~~~~~~~

0.1. Filter sequences
^^^^^^^^^^^^^^^^^^^^^^

0.2. Fetch ``.fasta``
^^^^^^^^^^^^^^^^^^^^^
Description:

+---------+-------------------------+-------------------------+
| IN:     | ``newfam_list.tsv``     | List of RNAcentral URSs |
+---------+-------------------------+-------------------------+
| script: | 00.get_fasta.py_                                  |
+---------+-------------------------+-------------------------+
| OUT:    |``newfam_seq.fasta``     |                         |
+---------+-------------------------+-------------------------+
| use:    |  ``python 00.get_fasta.py <IN.tsv> <OUT.fasta>``  |
+---------+-------------------------+-------------------------+

.. _00.get_fasta.py: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/nhmmer_approach2/00.get_fasta.py


1. ``nhmmer`` all vs all
~~~~~~~~~~~~~~~~~~~~~~~~
1.1. Run ``nhmmer``
^^^^^^^^^^^^^^^^^^^
Description:

+---------+-------------------------+------------------------------------+
| IN:     | ``newfam_seq.fasta``    | All sequences in ``.fasta`` format |
+---------+-------------------------+------------------------------------+
| script: | 01.a.newfam-nhmmer.sh_                                       |
+---------+-------------------------+------------------------------------+
| OUT:    |``newfam_nhmmer.out``    |  ``nhmmer`` stout                  |
|         +-------------------------+------------------------------------+
|         |``newfam_nhmmer.sto``    |  concatenated stockholm file       |
|         +-------------------------+------------------------------------+
|         |``newfam_nhmmer.tbl``    | ``nhmmer`` table output            |
+---------+-------------------------+------------------------------------+
| use:    |``01.newfam-nhmmer.sh <IN> <OUT.out> <OUT.sto> <OUT.tbl>``    |
+---------+-------------------------+------------------------------------+

.. _01.newfam-nhmmer.sh: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/nhmmer_approach2/00.get_fasta.py


1.2. Parse ``nhmmer`` table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Description:

+---------+-------------------------+------------------------------------+
| IN:     | ``newfam_nhmmer.tbl``   |  from 1.1                          |
+---------+-------------------------+------------------------------------+
| script: | 03.a.parse.py                                                |
+---------+-------------------------+------------------------------------+
| OUT:    |``newfam_nhmmer.tsv``    |                                    |
+---------+-------------------------+------------------------------------+
| use:    |``03.a.parse.py <IN.tbl> <OUT.tsv>``                          |
+---------+--------------------------------------------------------------+

.. _01.newfam-nhmmer.sh: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/nhmmer_approach2/00.get_fasta.py


1.3. Slice alignments
^^^^^^^^^^^^^^^^^^^^^
Description:

+---------+-------------------------+------------------------------------+
| **IN:** | ``newfam_nhmmer.sto``   |  from 1.1                          |
+---------+-------------------------+------------------------------------+
| script: | 02.slice_sto_nhmmer.py                                       |
+---------+--------------------------------------------------------------+
| use:    |``02.slice_sto_nhmmer.py <IN.sto>``                           |
+---------+-------------------------+------------------------------------+
| **OUT:**| ``URSxxxxxxxxxx.sto``   |                                    |
|         | ...                     |                                    |
+---------+-------------------------+------------------------------------+


2. Filter alignments
~~~~~~~~~~~~~~~~~~~~

2.1. Remove non significant
^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.2. Remove singletons
^^^^^^^^^^^^^^^^^^^^^^

3. Cluster groups
~~~~~~~~~~~~~~~~~

4. Clean alignments
~~~~~~~~~~~~~~~~~~~
4.1. Clean alignments
^^^^^^^^^^^^^^^^^^^^^
4.2. Pick best of repeated
^^^^^^^^^^^^^^^^^^^^^^^^^^

5. Select best alignment of group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
5.1. Easel cleaned alignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
5.2. Select best
^^^^^^^^^^^^^^^^

5. Make autoRfam
~~~~~~~~~~~~~~~~
