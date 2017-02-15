import sys
import re
import os

FILENAME = "./402.ali"
ROOTNAME = os.path.splitext(os.path.basename(FILENAME))[0]
PATHNAME = os.path.join(os.path.dirname(FILENAME), ROOTNAME)
os.mkdir(PATHNAME)


# open and read alignment
ALI = open(FILENAME)
ALICONTENT = ALI.read()
COMMPATT = re.compile(r"#=GR.*\n")
ALICONTENT = COMMPATT.sub("", ALICONTENT)
COMMPATT2 = re.compile(r"#=GC PP_cons.*\n")
ALICONTENT = COMMPATT2.sub("", ALICONTENT)
COMMPATT3 = re.compile(r"#=GC RF.*\n")
ALICONTENT = COMMPATT3.sub("", ALICONTENT)
# pattern to identify end of alignment, split
ENDPATT = re.compile("\/\/\n")
FILELIST = ENDPATT.split(ALICONTENT)

# pattern to get first sequence aka query, list names
NAMEPATT = re.compile(r'\n\nURS.{10}')
NAMES = []
for i in range(0, len(FILELIST) - 1):
    eachname = NAMEPATT.findall(FILELIST[i])
    NAMES.append(eachname[0])
# clean name
BAD = re.compile("\n\n")
for i in range(0, len(NAMES)):
    NAMES[i] = BAD.sub("", NAMES[i])
# add extension
NAMES = [s + ".sto" for s in NAMES]
# write files
for i in range(0, len(FILELIST) - 1):
    seqInfoFile = open(os.path.join(PATHNAME, NAMES[i]), 'w')
    seqInfoFile.write(FILELIST[i])
    seqInfoFile.write("//")
    seqInfoFile.close()
