# SIMPLE PROGRAMM WRITTEN IN PYTHON
# THIS PROGRAMM GIVES THE COORDINATES OF EVERY CDS FEATURE

# JOIN_CHAIN (5'3') = DIRECT CHAIN
# COMPLEMENT_CHAIN (3'5') = REVERSE CHAIN

# READCOORDS TAKES AN ANNOTATED EMBL FILE AS INPUT AND READS
# GENOMIC LENGTHS CDS FEATURES (JOIN AND COMPLEMENT CHAINS)
# AFTER IT WRITES A REPORT SHOWING ALL THE COORDINATES (BOTH CHAINS)
# IN 5'3' DIRECTION

# SHOW THE JOIN CHAIN AND REST THE TOTAL LENGTH OF THE GENOME MINUS
# THE COORDINATES OF COMPLEMENT CHAIN 

# "Complement_locus_tag" IS AN USEFUL TOOL FOR THE RESEARCHER IN ORDER
# TO LOCALIZATE EASY AND FAST THE RIGHT CDS COMPLEMENT FEATURE

#--------------------------------------------------------------------

# 1st STEP 
# IMPORT USED MODULES 

# FOR REGULAR EXPRESSIONS
import re

# FOR PASSING ARGUMENTS FROM LINUX COMMAND LINE
import sys

#--------------------------------------------------------------------

# 2nd STEP
# CREATE THE MAIN FUNCTION
# THIS FUNCTION RETRIEVES THE TOTAL LENGTH OF THE GENOME
# FROM THE ID LINE (first line into an annotated procariotic genome)
# WITH A REGULAR EXPRESSION

def Find_genome_size(lines):
    regex = r"^ID\s+.+\d+" # This regex gets the last number of ID line, which corresponds to total genome length
    for line in lines:
        if re.search(regex, str(line)): # re.search takes a regex and a string, and search for the regex into the string
            ID_line = re.search(regex, str(line))
            if re.search(r"\d+$",str(ID_line.group(0))):
                genome_size = re.search(r"\d+$",str(ID_line.group(0)))
                return genome_size.group(0)

#--------------------------------------------------------------------

# 3rd STEP
# OPEN FILE AND READ LINES

file_name = sys.argv[1]
file = open(file_name)
lines = file.readlines()
all_lines = "".join(lines)
genome_size = Find_genome_size(lines)

#--------------------------------------------------------------------

# 4th STEP
# STORE EVERY COMPLEMENT CDS FEATURE COORDINATES

regex = r"^FT\s+CDS\s+complement\(join\([0-9]+\.\.[0-9]+\)\)"
all_coords_complement = []
for line in lines:
    if re.search(regex, str(line)):
        CDS_line = re.search(regex, str(line))

        if re.search(r"\.[\d]+",str(CDS_line.group(0))):
            coord1 = re.search(r"\.[\d]+",str(CDS_line.group(0)))
            coord1 = re.search(r"\d+",str(coord1.group(0)))
            coord1 = int(genome_size) - int(coord1.group(0))

        if re.search(r"\d+\.",str(CDS_line.group(0))):
            coord2 = re.search(r"\d+\.",str(CDS_line.group(0)))
            coord2 = re.search(r"\d+",str(coord2.group(0)))
            coord2 = int(genome_size) - int(coord2.group(0))

        all_coords_complement.append([coord1,coord2])

#--------------------------------------------------------------------

# 5th STEP
# STORE EVERY JOIN CDS FEATURE COORDINATES

regex = r"^FT\s+CDS\s+join\([0-9]+\.\.[0-9]+\)"
all_coords_join = []
for line in lines:
    if re.search(regex, str(line)):
        CDS_line = re.search(regex, str(line))

        if re.search(r"\.[\d]+",str(CDS_line.group(0))):
            coord1 = re.search(r"\.[\d]+",str(CDS_line.group(0)))
            coord1 = re.search(r"\d+",str(coord1.group(0)))


        if re.search(r"\d+\.",str(CDS_line.group(0))):
            coord2 = re.search(r"\d+\.",str(CDS_line.group(0)))
            coord2 = re.search(r"\d+",str(coord2.group(0)))


        all_coords_join.append([coord2.group(0),coord1.group(0)])


#--------------------------------------------------------------------

# 6nd STEP
# GET EVERY COMPLEMENT LOCUS TAG (in order to identify in the file the
# reverse chain of CDS Complement Feature)

complement_locus_tags = []
regex = r"^FT\s+CDS\s+complement.*\n(.*\n)*?^FT\s+\/locus\_tag\=\"(E\d+\C\_\d+)"
if re.findall(regex, str(all_lines), re.MULTILINE):
    locus_tag = re.findall(regex, str(all_lines), re.MULTILINE)
    for tag in locus_tag:

        complement_locus_tags.append(tag[1])


#--------------------------------------------------------------------

# 7nd STEP
# WRITE A REPORT FAVOURING EXCEL EXPORTING

if len(all_coords_complement) > len(all_coords_join):
    bigger = all_coords_complement
    lower = all_coords_join
    print "COORDINATES IN JOIN CHAIN (5'3') ; COORDINATES IN COMPLEMENT CHAIN (REVERSED) (3'5') ; COMPLEMENT LOCUS TAG ANNOTATED"
    for i in range(len(bigger)):
        try:
            print lower[i][0]," - ",lower[i][1]," ; ",bigger[-i-1][0]," - ",bigger[-i-1][1]," ; ",complement_locus_tags[-i-1]
        except IndexError:
            print "\t\t     ; ", bigger[-i-1][0]," - ",bigger[-i-1][1]," ; ",complement_locus_tags[-i-1]
else:
    bigger = all_coords_join
    lower = all_coords_complement
    print "COORDINATES IN COMPLEMENT CHAIN (REVERSED) (3'5') ; COORDINATES IN JOIN CHAIN (5'3') ;  COMPLEMENT LOCUS TAG ANNOTATED"
    for i in range(len(bigger)):
        try:
            print lower[i][0]," - ",lower[i][1]," ; ",bigger[-i-1][0]," - ",bigger[-i-1][1]," ; ",complement_locus_tags[-i-1]
        except IndexError:
            print "\t\t     ; ", bigger[-i-1][0]," - ",bigger[-i-1][1]

       
