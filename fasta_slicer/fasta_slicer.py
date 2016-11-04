import sys
from Bio import SeqIO

output_length = int(sys.argv[1])
input_file = sys.argv[2]

#FROM http://biopython.org/wiki/Split_large_file
def batch_iterator(iterator, batch_size):
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.next()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch

record_iter = SeqIO.parse(open(input_file),"fasta")
for i, batch in enumerate(batch_iterator(record_iter, output_length)):
    filename = input_file+"group_%i.fasta" % (i + 1)
    handle = open(filename, "w")
    count = SeqIO.write(batch, handle, "fasta")
    handle.close()
    print("Wrote %i records to %s" % (count, filename))
