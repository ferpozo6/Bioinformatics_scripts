import sys
import re
from Bio import SeqIO

file_name = str(input("Type the file you want to read: "))
file = open(file_name)
for record in SeqIO.parse(file, "embl"):
    print record.id," - ",len(record)

file.close()
