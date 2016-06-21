# PARSING EMBL FILES

# Juan Jimenez Sanchez
# Fernando Pozo Ocampo

# This program's goal is to parse an embl file. Current version just retrieves every CDS feature coordinates
# both in direct (join) and reverse (complement) chains. It also stores every locus tag ID for every reverse
# chain CDS feature. In order to show CDS features from left to right, direct chain feature coords are shown 
# in 5'->3'sense, while reverse chain feature coords are shown in 3'->5' sense. To accomplish that, reverse
# chain feature 3'->5' coords are obtained from a simple formula:
#
#	3'->5' reverse chain feat. coords = genome length - 5'->3' reverse chain feat. coords
#
#


#-----------------------------------------------------------------------------------------------------------------------------------------------
# Before starting --> Importing useful modules

import re # We are going to use regex
import sys # We will pass filename as a command line argument to this program


#-----------------------------------------------------------------------------------------------------------------------------------------------
# 1st step --> Create functions
            
# Search_pattern(pattern, text) --> Makes regex search more readable
# 				    As re.search, uses a pattern and a text as input

def Search_pattern(pattern, text):
    return re.search(pattern, str(text))

# Search_all_patterns(pattern, text) --> Older brother of previous function
#					 Works the same way, but retrieves every hit found

def Search_all_patterns(pattern, text):
    return re.findall(pattern, str(text), re.MULTILINE)

# Find_genome_size(lines) --> Lines correspond to file lines
#			      It uses previous functions to find genome/chromosome size

def Find_genome_size(lines):
    regex = r"^ID\s+.+\d+"
    for line in lines:
        ID_line = Search_pattern(regex, str(line))
	if ID_line != None:
        	genome_size = Search_pattern(r"(\d+)$", str(ID_line.group(0)))
        	return genome_size.group(0)


#-----------------------------------------------------------------------------------------------------------------------------------------------
# 2nd step --> Open file, read lines, and get the genome size

file_name = sys.argv[1]
file = open(file_name)
lines = file.readlines()   # We want both a list with every file line,
all_lines = "".join(lines) # and a string with whole file
genome_size = Find_genome_size(lines)


#-----------------------------------------------------------------------------------------------------------------------------------------------
# 3rd step --> Search for CDS feature coords in complement (reverse) chain

regex = r"^FT\s+CDS\s+complement\(join\([0-9]+\.\.[0-9]+\)\)"
all_coords_complement = []
for line in lines:
    CDS_line = Search_pattern(regex, str(line)) # At first, every line is stored in 'CDS_line'
    if CDS_line != None: # But, except for true CDS lines, the rest of them will have assigned a value of 'None'. 
			 # This way we get rid of false CDS lines
        coord1 = Search_pattern(r"\.(\d+)",CDS_line.group(0))
        coord1 = int(genome_size) - int(coord1.group(1)) # Here we make use of the formula aforementioned
        coord2 = Search_pattern(r"(\d+)\.",CDS_line.group(0))
        coord2 = int(genome_size) - int(coord2.group(1)) # Both for starting and ending coordinate
    	all_coords_complement.append([coord1,coord2]) # Coords are stored from lower to bigger
        

#-----------------------------------------------------------------------------------------------------------------------------------------------
# 4th step --> Search for CDS feature coords, this time in join (direct) chain

regex = r"^FT\s+CDS\s+join\([0-9]+\.\.[0-9]+\)"
all_coords_join = []
for line in lines:
    CDS_line = Search_pattern(regex, str(line))
    if CDS_line != None:
    	coord1 = Search_pattern(r"\.(\d+)",CDS_line.group(0))
    	coord1 = coord1.group(1) # With direct chain, we don't need to use the aforementioned formula
    	coord2 = Search_pattern(r"(\d+)\.",CDS_line.group(0))
    	coord2 = coord2.group(1)
    	all_coords_join.append([coord2,coord1]) # To store coords from lower to bigger, we change the order in which we store them
        

#-----------------------------------------------------------------------------------------------------------------------------------------------
# 5th step --> Search for complement (reverse) chain CDS feature locus tags

complement_locus_tags = []
regex = r"^FT\s+CDS\s+complement.*\n(.*\n)*?^FT\s+\/locus\_tag\=\"(E\d+\C\_\d+)"
locus_tags = Search_all_patterns(regex, all_lines) # This time we search them all in string 'all_lines', not in list 'lines', as we
						   # are using newlines in our regex
if locus_tags != None:
    for tag in locus_tags:
    	complement_locus_tags.append(tag[1])


#-----------------------------------------------------------------------------------------------------------------------------------------------
# 6th step --> Print Excel-friendly report

# We have to be careful when iterating, as we want to go along the bigger list between 'all_coords_complement' and 'all_coords_join'.
# This is why we check which one is the bigger. If complement coords list is bigger, we want to print locus tags even when join coords
# list is empty. But, if join list is the bigger one, we don't want to print locus tags, as they belong to complement coords list, so they
# will be depleted while join coords are still being printed. That is why we check so carefully all this things in code below.

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
