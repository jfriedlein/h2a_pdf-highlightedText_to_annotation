# Call from command line as:
# python -c 'from h2a_commander import h2a_commander; h2a_commander("Bruenig.pdf")'

import sys

def h2a_commander ( input_filename, output_mode='h2a', update_procedure='update_new', autoMarker=' >a> ' ):
    
    
    sys.path.append('./h2a_functions')
    from h2a_highlightedText_to_annotation import h2a_highlightedText_to_annotation
    
    h2a_highlightedText_to_annotation ( input_filename, output_mode, update_procedure, autoMarker )
