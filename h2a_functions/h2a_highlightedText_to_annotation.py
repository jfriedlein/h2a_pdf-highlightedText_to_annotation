# The base code is inspired from [https://medium.com/@vinitvaibhav9/extracting-pdf-highlights-using-python-9512af43a6d]
# Required modules:
#pip install fitz
#pip install PyMuPDF
# @todo
# - hyphen or no hyphen: Detect word at line break via the sort_rectangles sort_matrix
#                        and then compare the word with and without hyphen to an English dictionary
# - top to bottom: annotations are processed in the order they have been saved in the pdf,
#                  this is irrelevant for output_mode 'h2aX'. But when saving to a text file it
#                  would be nice to get them sequentially. For this we first extract all annotations
#                  of a page and after that loop over them. This will later enable some kind of sorting
#                  (be aware of single vs double column for top-down sorting)

# Import "fitz" for loading etc. pdfs (seems to also contain PyMuPDF)
import fitz
# Import "datetime" to get current date and time (for H2A-protocol)
import datetime
import pytz
# Import "time" to get processing time (for H2A-protocol)
import time
# Import "os" for splitting the path with the operator specific file separator
import os

# Load the h2a modules from the subfolder "h2a_functions"
import sys
sys.path.append('./h2a_functions')
from sort_rectangles import sort_rectangles
from is_on_same_line import is_on_same_line
from containment_of_a_in_b import containment_of_a_in_b
#from annot_toBe_changed import annot_toBe_changed
from annot_toBe_changed_time import annot_toBe_changed_time
from extract_comment_text import extract_comment_text
from process_H2A_protocol import process_H2A_protocol
from update_h2a_logfile import update_h2a_logfile
from annot_cleaned import annot_cleaned
from retrieve_H2A_protocol import retrieve_H2A_protocol
from get_new_title import get_new_title
from get_output_file_annot import get_output_file_annot

# Choose the update procedure update_procedure:
# - 'update_all': overwrite extracted text if '>a>' or '>p>' or none/new, also removes 'p' marker
# - 'update_auto': do not touch 'p', only modify 'a' and none/new
# - 'update_new': do not touch 'p' or 'a', only none/new (recommended)
# Choose the output mode output_mode:
# - 'h2a': write highlighted text into input pdf
# - 'h2a_annot': write highlighted text into copy of input pdf, new filename ends with "_annot.pdf"
# - 'h2a_txt': write highlighted dtext into separate text file
# Choose whether a marker autoMarker should be placed after the extracted text like
# "[highlighted text] >a> [existing text]"
# alternative for instance "[highlighted text]: [existing text]" using autoMarker=': '
# or none autoMarker=''

def h2a_highlightedText_to_annotation ( input_file, output_mode='h2a', update_procedure='update_new', autoMarker=' >a> ' ):
    
    ## CODE
    # h2a-version
    h2a_version = 'V2.0'
    
    title_suffix = '_h2a'
    
    # Build the name of input_filename which excludes the file extensions
    # remove file extension
    # [https://stackoverflow.com/questions/3548673/how-can-i-replace-or-strip-an-extension-from-a-filename-in-python]
    input_filename = os.path.splitext(input_file)[0]
    
    # Get name of pdf (head of path)
    pdf_name = os.path.split(input_file)[1]
    
    time_current = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime("D:%Y%m%d%H%M%S%z")
    time_current = time_current[0:19]+"'"+time_current[19:]

    print("Processing the pages of '"+pdf_name+"' ...")
    # Start timer to measure processing time
    tic = time.process_time()
    
    # Open the pdf into "doc"
    doc = fitz.open(input_file)
    
    # number of pages (for logfile)
    n_pages = len(doc)
    
    # Read H2A-protocol
    H2A_protocol = retrieve_H2A_protocol( doc[0] )
    
    # For the txt output mode, open an empty txt file
    if ( output_mode == 'h2a_txt' ):
        f = open(input_filename+'_annot.txt', 'w')
    
    # Loop over each page
    annot_counter = 0
    for page in doc:
        # list to store the annotations and the co-ordinates of all highlights
        annot_cleaned_list = list()
        for annot in page.annots():
            # Only consider "Highlight" (type=8) annotations
            if ( annot.type[0] == 8 ):
                # Get all coordinates of the vertices that span the highlight (rectangles)
                all_coordinates = annot.vertices
                highlight_coords = []
                n_rects = 0
                # @todo-clean Always using the code in "else" should do no harm (is that much slower?)
                # if the annotations contains only four vertices (one rectangle)
                # @note How to work with Rect [https://pymupdf.readthedocs.io/en/latest/rect.html]
                if len(all_coordinates) == 4:
                    highlight_coords = fitz.Quad(all_coordinates).rect
                    n_rects = 1
                # if the annotation contains multiple rectangles
                else:
                    all_coordinates = [all_coordinates[x:x+4] for x in range(0, len(all_coordinates), 4)]
                    for i in range(0,len(all_coordinates)):
                        highlight_coord = fitz.Quad(all_coordinates[i]).rect
                        highlight_coords.append(highlight_coord)
                        n_rects = n_rects + 1
                    # Sort the rectangles according to the reading flow
                    highlight_coords = sort_rectangles( highlight_coords )
                # Append an annotation object containing the annotation, the coords and the number of rectangles
                annot_cleaned_list.append( annot_cleaned(annot, highlight_coords, n_rects) )
            
        # Retrieve all words on this page including their coordinates
        all_words_on_page = page.get_text_words()
        
        # Loop over all annotations
        for annot_i in annot_cleaned_list:
            # Retrieve the text that is already contained in the annotation
            # annot_text = annot_i.annotation.info['content']
            # First check whether the annotation is to be changed, this depends
            # on the update procedure and the marker in the annot_text
            #if annot_toBe_changed( annot_text, output_mode, update_procedure ):
            if annot_toBe_changed_time( annot_i.annotation, time_current, H2A_protocol, output_mode, update_procedure ):
                highlight_text = []
                # Loop over all rectangles that belong to this annotation (adding all text into a single annotation)
                for i_rect in range(0,annot_i.n_rects):
                    # @todo-clean How to merge these two cases, maybe save the coordinates nicer or call a method on each annotation
                    if annot_i.n_rects == 1:
                        h_rect = annot_i.coords
                    else:
                        h_rect = annot_i.coords[i_rect][0:4]
                    # Assign the x,y and min,max coordinates of the bounding box for this highlight
                    # Maybe this can directly be retrieved from annot.vertices? without the intermediate fitz.Quad.rect step?
                    xmin_h, ymin_h, xmax_h, ymax_h = h_rect[0], h_rect[1], h_rect[2], h_rect[3]
                    # Loop over all words on this page
                    for w in all_words_on_page:
                        # Retrieve the word as text
                        # @todo Improve encoding to be able to read more symbols and special characters
                        current_word = w[4]
                        # Assign the x,y and min,max coordinates of the current word
                        xmin_w, ymin_w, xmax_w, ymax_w = w[0],w[1],w[2],w[3]
                        # Compute the coverage to see whether the current word lies within the highlight bounding box
                        coverage = containment_of_a_in_b( xmin_w, ymin_w, xmax_w, ymax_w, xmin_h, ymin_h, xmax_h, ymax_h )
                        # If the current word lies by 30% in the highlight
                        # and it is in the same line, we see this as contained
                        if ( coverage > 0.3 and is_on_same_line( fitz.Rect(w[0:4]), fitz.Rect(h_rect[0:4]) ) ):
                            highlighted_word = current_word
                            # Debugging
                            #highlighted_word = highlighted_word+'_'+str(round(coverage,2))
                            # Append the current word to a list of yet not connected words
                            highlight_text.append(highlighted_word)
                # Join the words in the highlight_text for the current annotation by spaces
                # Details: [https://pymupdf.readthedocs.io/en/latest/annot.html#Annot.info]
                # @todo When a word is split over multiple lines like "split-\nting", we can remove the hyphen, but e.g. not for "FEM-method"
                highlighted_phrase = " ".join(highlight_text)
                # Extract comment part (after '>*>') from annot_text
                comment_text = extract_comment_text( annot_i.annotation, H2A_protocol, title_suffix )
                # Build new content of annotation from detected highlighted text and existing comment_text
                if ( len(comment_text)==0 ):
                    output_content = highlighted_phrase
                else:
                    output_content = highlighted_phrase + autoMarker + comment_text
                if ( output_mode in {'h2a','h2a_annot'} ):
                    new_title = get_new_title( annot_i.annotation, title_suffix )
                    # The text content of the current annotation annot_i is replaced by
                    # the detected highlighted text with the marker '>a>' followed by the existing text
                    annot_i.annotation.set_info( content=output_content, modDate=time_current, title=new_title )
                elif ( output_mode == 'h2a_txt' ):
                    f.write(output_content+'\n')
                annot_counter += 1
            
    time_processing = time.process_time() - tic
    print("... finished processing the pages.")
    
    
    ## Process H2A protocol
    process_H2A_protocol( annot_counter, time_current, time_processing, doc[0], h2a_version )
    
    
    ## Save output
    if ( output_mode == 'h2a_txt' ):
        f.close()
    # Save the pdf with the modified annotations into the input_file overwriting it
    elif ( output_mode == 'h2a' ):
        doc.saveIncr()
    # Save the pdf with the modified annotations into a separate output_file
    elif ( output_mode == 'h2a_annot' ):
        output_file = get_output_file_annot( input_file )
        doc.save(output_file)
    
    
    ## Update h2a-logfile
    update_h2a_logfile( time_current, pdf_name, h2a_version, annot_counter, n_pages, time_processing )    
