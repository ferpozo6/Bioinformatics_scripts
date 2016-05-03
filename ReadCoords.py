# SIMPLE PROGRAMM WRITTEN IN PYTHON
# THIS PROGRAMM 

import re
import sys

def Find_genome_size(lines):
    regex = r"^ID\s+.+\d+"
    for line in lines:
        if re.search(regex, str(line)):
            ID_line = re.search(regex, str(line))
            if re.search(r"\d+$",str(ID_line.group(0))):
                genome_size = re.search(r"\d+$",str(ID_line.group(0)))
                return genome_size.group(0)

file_name = sys.argv[1]
file = open(file_name)
lines = file.readlines()
all_lines = "".join(lines)
genome_size = Find_genome_size(lines)
# print genome_size
# print file.readlines()
regex = r"^FT\s+CDS\s+complement\(join\([0-9]+\.\.[0-9]+\)\)"
all_coords_complement = []
for line in lines:
    if re.search(regex, str(line)):
        CDS_line = re.search(regex, str(line))
        # print CDS_line.group(0) # print CDS_lines
        if re.search(r"\.[\d]+",str(CDS_line.group(0))):
            coord1 = re.search(r"\.[\d]+",str(CDS_line.group(0)))
            coord1 = re.search(r"\d+",str(coord1.group(0)))
            coord1 = int(genome_size) - int(coord1.group(0))
            #print coord1
        if re.search(r"\d+\.",str(CDS_line.group(0))):
            coord2 = re.search(r"\d+\.",str(CDS_line.group(0)))
            coord2 = re.search(r"\d+",str(coord2.group(0)))
            coord2 = int(genome_size) - int(coord2.group(0))
            #print " --> ", coord2
        all_coords_complement.append([coord1,coord2])
        #print coord1," - ",coord2

##print "COORDINATES IN COMPLEMENT CHAIN (REVERSED)"
##for num in reversed(all_coords_complement):
##    print num[0]," - ",num[1]


regex = r"^FT\s+CDS\s+join\([0-9]+\.\.[0-9]+\)"
all_coords_join = []
for line in lines:
    if re.search(regex, str(line)):
        CDS_line = re.search(regex, str(line))
        # print CDS_line.group(0) # print CDS_lines
        if re.search(r"\.[\d]+",str(CDS_line.group(0))):
            coord1 = re.search(r"\.[\d]+",str(CDS_line.group(0)))
            coord1 = re.search(r"\d+",str(coord1.group(0)))
            #coord1 = int(genome_size) - int(coord1.group(0))
            #print coord1
        if re.search(r"\d+\.",str(CDS_line.group(0))):
            coord2 = re.search(r"\d+\.",str(CDS_line.group(0)))
            coord2 = re.search(r"\d+",str(coord2.group(0)))
            #coord2 = int(genome_size) - int(coord2.group(0))
            #print " --> ", coord2
        all_coords_join.append([coord2.group(0),coord1.group(0)])
        #print coord1," - ",coord2

# print all_lines
complement_locus_tags = []
regex = r"^FT\s+CDS\s+complement.*\n(.*\n)*?^FT\s+\/locus\_tag\=\"(E\d+\C\_\d+)"
if re.findall(regex, str(all_lines), re.MULTILINE):
    locus_tag = re.findall(regex, str(all_lines), re.MULTILINE)
    for tag in locus_tag:
        #print tag[1]
        complement_locus_tags.append(tag[1])



print "COORDINATES IN JOIN CHAIN (5'3') ; COORDINATES IN COMPLEMENT CHAIN (REVERSED) (3'5') ; COMPLEMENT LOCUS TAG ANNOTATED"
for i in range(len(all_coords_complement)):
    try:
        print all_coords_join[i][0]," - ",all_coords_join[i][1]," ; ",all_coords_complement[-i-1][0]," - ",all_coords_complement[-i-1][1]," ; ",complement_locus_tags[-i-1]
    except IndexError:
        print "\t\t     ; ", all_coords_complement[-i-1][0]," - ",all_coords_complement[-i-1][1]," ; ",complement_locus_tags[-i-1]
        
# print len(all_coords_join)," - ",len(all_coords_complement)," - ",len(complement_locus_tags)

