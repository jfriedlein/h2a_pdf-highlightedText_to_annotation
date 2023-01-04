# Clean the workspace and the console for a fresh start as in Matlab "clear,clc"
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

from h2a_commander import h2a_commander
h2a_commander("Bruenig_short_annot_mod", output_mode='h2a_annot', update_procedure='update_new')
