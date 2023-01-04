import fitz
# Load the h2a modules from the subfolder "h2a_functions"
import sys
sys.path.append('./h2a_functions')
from extract_comment_text import extract_comment_text
from retrieve_H2A_protocol import retrieve_H2A_protocol

def h2a_unddo( input_file ):
    # Open the pdf into "doc"
    doc = fitz.open(input_file)
    
    title_suffix = '_h2a'
    
    # Read H2A-protocol
    H2A_protocol = retrieve_H2A_protocol( doc[0] )
    
    protocol_deleted = False
    
    for i_page, page in enumerate(doc):
        for annot in page.annots():
             if ( annot.type[0] == 8 ):
                 title = annot.info['title']
                 if ( title_suffix in title ):
                     # Extract comment part (after '>*>') from annot_text
                     comment_text = extract_comment_text( annot, H2A_protocol, title_suffix ) 
                     # replace content of annotation by original comment text and remove title suffix
                     annot.set_info( content=comment_text, title=title[0:len(title)-len(title_suffix)] )
             if ( i_page==0 and protocol_deleted==False ):
                # delete h2a protocol
                # If the annotation content contains the catch phrase, we have found the protocol
                if ( 'H2A-protocol' in annot.info['content'] ):
                    page.delete_annot(annot)
                    protocol_deleted = True
                    
    doc.saveIncr()