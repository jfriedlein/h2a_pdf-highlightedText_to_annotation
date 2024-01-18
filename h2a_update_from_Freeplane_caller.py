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

from h2a_functions.h2a_update_from_freeplane import h2a_update_from_freeplane

# run e.g. as:
# python3 h2a_update_from_freeplane_caller.py "freeplane-tmp-file.tmp"
# or via a pyinstaller executable
# h2a_update_from_freeplane_caller "freeplane-tmp-file.tmp"

# Extract the full path and filename of the Freeplane output (e.g. h2a_freeplane-changes.tmp) from the command line option, here "%20" might have been used to replace blankspaces
path_file = sys.argv[1].replace("%20"," ")

h2a_update_from_freeplane( path_file )
