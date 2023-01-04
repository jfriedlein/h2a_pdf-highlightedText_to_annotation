# Clean the workspace and the console for a fresh start as in Matlab "clear,clc"
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

import sys
sys.path.append('./h2a_functions')
from h2a_highlightedText_to_annotation import h2a_highlightedText_to_annotation

## USER-INPUT
# Enter the filename of the pdf without the file extension
input_filename = "Bruenig" #"test pdfs/Miehe"
# Choose the update procedure:
# - 'update_all': overwrite extracted text if '>a>' or '>p>' or none/new, also removes 'p' marker
# - 'update_auto': do not touch 'p', only modify 'a' and none/new
# - 'update_new': do not touch 'p' or 'a', only none/new (recommended)
update_procedure = 'update_new'
# Choose the output mode
# - 'h2a': write highlighted text into input pdf
# - 'h2a_annot': write highlighted text into copy of input pdf, new filename ends with "_annot.pdf"
# - 'h2a_txt': write highlighted dtext into separate text file
output_mode = 'h2a'
# Choose whether a marker should be placed after the extracted text like
# "[highlighted text] >a> [existing text]"
# alternative for instance "[highlighted text]: [existing text]" using autoMarker=': '
# or none autoMarker=''
autoMarker = ' >a> '

#h2a_highlightedText_to_annotation ( input_filename, output_mode, update_procedure, autoMarker )
h2a_highlightedText_to_annotation ( input_filename )