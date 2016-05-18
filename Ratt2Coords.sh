# RATT USAGE --> ratt embl .fna annotated Assembly

# default values
PRGNAME=`basename $0`
RATT_MODE='Assembly'
REF_EMBL_FILE='reference.embl'
QUERY_FASTA_FILE='unannotated.fasta'


# RATT Parameters:
#	1- embl folder containing .embl file reference
#	2- query fasta (.fna) file (in working dir) containing contigs to be annotated
#	3- ratt mode (Assembly, Strain, Species)

# PROGRAM USAGE --> allInOne -r reference.embl -i query.fasta -m Assembly

function usage()
{
	echo 'To call the program, type the following in the command line:'
	echo "bash $PRGNAME -m RATT_mode -r Reference_file.embl -i Query_file.fasta"
	echo 'RATT modes implemented: Assembly'

}

function quickcp()
{
    # if the origin file does not exist, do nothing
    if [ ! -e $1 ] ; then echo "$1 does  not exist!" ; fi
    # if the destination is not a directory
    if [ ! -d $2 ] ; then
        # if the destination file does not exits, copy 
        if [ ! -e $2 ] ; then
            cp $1 $2
        # if the destination exists, do nothing
        else
            echo "$2 exists!"
        fi
    # if the destination is a directory
    else
        # if the destination file does not exist, copy
        if [ ! -e $2/`basename $1` ] ; then
            cp $1 $2
        # if it does exist, do nothing
        else
            echo $2/`basename $1` "exists!"
        fi
    fi
}


if [ $# -eq 1 ] ; then usage ; fi

TEMP=`getopt -o r:m:i:hv \
     --long reference:,method:,input:,help,verbose \
     -n "$0" -- "$@"`

# an invalid option was given
if [ $? != 0 ] ; then usage >&2 ; exit 1 ; fi

# Note the quotes around `$TEMP': they are essential!
#  the set command takes any arguments after the options (-- signals the end
#  of the options) and assigns them to positional parameters $0..$n.
#  We pass set through eval so that bash will honor embedded quotes in the
#  string, i.e.
#	whithout eval, "ab cd" is split at the space into "ab and cd"
#	with eval, bash honors que quotes and gives "ab cd" as a single value
#
eval set -- "$TEMP"

while true ; do
        case "$1" in
                -h|--help) 
                    usage ; shift ;;

                -i|--input)
                    QUERY_FASTA_FILE="$2" ; shift 2 ;;
                    
                -r|--reference)
                    REF_EMBL_FILE="$2" ; shift 2 ;;
                    
		-m|--method)
		    RATT_MODE="$2" ; shift 2 ;;
		    
                -v|--verbose)
		   VERBOSE='yes' ; shift ;;
                --) shift ; break ;;
                *) echo "$0: Internal error!" >&2 ; usage ; exit 1 ;;
        esac
done


if [ $RATT_MODE != 'Assembly' ]; then echo 'Only Assembly mode is implemented in current version'; exit; fi

echo "Would you like to erase all files created by RATT after program execution? (y/n) --> "
read erase 

TRIAL_DIR="Ratt2Coords"
mkdir -p $TRIAL_DIR
quickcp $REF_EMBL_FILE $TRIAL_DIR
quickcp $QUERY_FASTA_FILE $TRIAL_DIR
quickcp ReadCoords003.py $TRIAL_DIR
cp ratt/* $TRIAL_DIR
cd $TRIAL_DIR

RATT_HOME=`pwd`
export RATT_HOME

if [ ! $RATT_MODE ]; then RATT_MODE="Assembly"; fi

EMBL_dir="embl"
if [ ! -d $EMBL_dir ] ; then mkdir -p $EMBL_dir ; fi

quickcp $REF_EMBL_FILE $EMBL_dir
bash start.ratt.sh embl $QUERY_FASTA_FILE annotated $RATT_MODE

REF_EMBL_FILENAME="${REF_EMBL_FILE%.*}"
CREATED_FILE="annotated.$REF_EMBL_FILENAME.NOTTransfered.embl"
if [ ! -e $CREATED_FILE ]; then echo "RATT didn't create any file. Aborting Execution"; exit; fi

EXCEL_FILE="annotated.$REF_EMBL_FILENAME.NOTTransfered.xls"

python2.7 ReadCoords003.py $CREATED_FILE > $EXCEL_FILE
echo "$EXCEL_FILE created"

quickcp $EXCEL_FILE ..
echo "$EXCEL_FILE copied back to working directory"
cd ..
if [ $erase == 'y' ]; then rm -rf $TRIAL_DIR; fi 



