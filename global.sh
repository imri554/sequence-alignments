# This example shell script directly calls the python interpreter
# on a hypothetical python script that will do a global alignment.
# It also passes the three arguments that this script is called with.
# The three arguments will be, in this order, the path (absolute or relative)
# to the sequences file, the path to the matrix file, and the gap penalty.
# You'll need to edit this file for the language of your choosing.
# Come to office hours if you need additional clarification.
python global.py ${1} ${2} ${3}
