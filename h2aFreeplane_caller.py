# Clean the workspace and the console for a fresh start as in Matlab "clear,clc"
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

import os
import fitz

import sys
from h2a_functions.h2a_highlightedText_to_annotation import h2a_highlightedText_to_annotation

# run e.g. as:
# python3 h2aFreeplane_caller.py "pdf-file.pdf" "tmp-file.tmp"
# or via a pyinstaller executable
# h2aFreeplane_caller "pdf-file.pdf" "tmp-file.tmp"

# Extract the full path and filename of the pdf from the command line option, here "%20" might have been used to replace blankspaces
# @todo Do we need to remove the file extension for h2a-Freeplane?
input_filename = sys.argv[1].replace("%20"," ")
# Extract the full path and filename of the output file for Freeplane, e.g. "h2a_pdf-output.tmp"
tmp_directory = "./h2a_pdf-output.tmp"
if ( len(sys.argv)>=3 ):
    tmp_directory = sys.argv[2].replace("%20"," ")
# Output mode is fixed to Freeplane
output_mode = 'h2a_freeplane'
## USER-Parameters
# Choose the update procedure:
# - 'update_all_removeCommentText'
# - 'update_all': overwrite extracted text if '>a>' or '>p>' or none/new, also removes 'p' marker
# - 'update_auto': do not touch 'p', only modify 'a' and none/new
# - 'update_new': do not touch 'p' or 'a', only none/new (recommended)
update_procedure = 'update_new'
if ( len(sys.argv)>=4 ):
    if ( sys.argv[3] in ['update_new','update_auto','update_all','update_all_removeCommentText'] ):
        update_procedure = sys.argv[3]
    else:
        print("h2aFreeplane_caller<< Unknown update_procedure="+sys.argv[3])
        
# Choose whether a marker should be placed after the extracted text like
# "[highlighted text] >a> [existing text]"
# alternative for instance "[highlighted text]: [existing text]" using autoMarker=': '
# or none autoMarker=''
autoMarker = ' >a> '

h2a_highlightedText_to_annotation ( input_filename, output_mode, update_procedure, autoMarker, tmp_directory )