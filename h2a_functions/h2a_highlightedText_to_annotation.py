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

import codecs

# Load the h2a modules from the subfolder "h2a_functions"
import sys
from h2a_functions.sort_rectangles import sort_rectangles
from h2a_functions.is_on_same_line import is_on_same_line
from h2a_functions.containment_of_a_in_b import containment_of_a_in_b
from h2a_functions.annot_toBe_changed_time import annot_toBe_changed_time
from h2a_functions.extract_comment_text import extract_comment_text
from h2a_functions.process_H2A_protocol import process_H2A_protocol
from h2a_functions.update_h2a_logfile import update_h2a_logfile
from h2a_functions.annot_cleaned import annot_cleaned
from h2a_functions.retrieve_H2A_protocol import retrieve_H2A_protocol
from h2a_functions.get_new_title import get_new_title
from h2a_functions.get_output_file_annot import get_output_file_annot

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

def h2a_highlightedText_to_annotation ( input_file, output_mode='h2a', update_procedure='update_new', autoMarker=' >a> ', tmp_pathFile='./h2a_pdf-output.tmp' ):
    
    ## CODE
    # h2a-version
    h2a_version = 'V2.0'
    
    title_suffix = '_h2a'
    
    entry_separator = ' ;x; '
    ES = entry_separator
    line_break_replacer = ' ;xnx; '

    # @note These delimiters are used, in addition to the default blankspace, to spread the continuous text in separate words.
    #       This is a double-edged sword as sometimes it is not desired to split a word at these places. E.g. splitting at "." 
    #       might make sense for mail addresses, but destroys "0.2" as "0 2". Moreover, "The “word” strings will not contain any 
    #       delimiting character." [https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_text], which is problematic, 
    #       because you might want to detect the words from "table/desktop" as "table" and "desktop" thus using "/" as delimiter, 
    #       but if the entire string shall be read you want "table/desktop" and not "table desktop".
    # @todo What we want is detect words by custom delimiters, but not removing them from the text.
    delimiters_to_detect_words_in_PDF = ""

    list_of_punctuationMarks_that_are_removed_if_leadingTrailing = [",",".",";"]
    
    # Build the name of input_filename which excludes the file extensions
    # remove file extension
    # [https://stackoverflow.com/questions/3548673/how-can-i-replace-or-strip-an-extension-from-a-filename-in-python]
    input_filename = os.path.splitext(input_file)[0]
    
    # Get name of pdf (head of path)
    pdf_name = os.path.split(input_file)[1]
    
    # For the directory to the h2a-logfile extract the directory from the path to the h2a-Freeplane tmp file
    path_to_tmp_directory = os.path.dirname(tmp_pathFile)
    
    # Determine the current time and format it as times are formatted in PDFs
    # @note "time_current" is used for all processed annotations and kept constant during the entire execution of this function
    time_current = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime("D:%Y%m%d%H%M%S%z")
    time_current = time_current[0:19]+"'"+time_current[19:]

    print("h2a_highlightedText_to_annotation<< Processing the pages of '"+pdf_name+"' ...")
    # Start timer to measure processing time
    tic = time.process_time()
    
    # Open the pdf into "doc"
    doc = fitz.open(input_file)
    
    # Read number of pages (for logfile)
    n_pages = len(doc)
    
    # Read H2A-protocol
    H2A_protocol = retrieve_H2A_protocol( doc[0] )
    
    # For the txt output mode, open an empty txt file, use utf-8 to capture special characters [https://stackoverflow.com/questions/491921/unicode-utf-8-reading-and-writing-to-files-in-python]
    if ( output_mode == 'h2a_txt' ):
        f = codecs.open(input_filename+'_annot.txt', 'w', "utf-8")
    elif ( output_mode == 'h2a_freeplane' ):
        f = codecs.open(tmp_pathFile, "w", "utf-8")
        
    # Loop over each page
    # Count the number of processed annotations
    # @todo What to count for h2a_freeplane?
    annot_counter = 0
    for page in doc:
        # list to store the annotations and the coordinates of all highlights on this page "page"
        annot_cleaned_list = list()
        for annot in page.annots():
            # Only consider "Highlight" (type=8) annotations here [https://pymupdf.readthedocs.io/en/latest/vars.html#annotationtypes]
            # For "Note"/"Text" annotations there is no highlighted text
            if ( annot.type[0] == fitz.PDF_ANNOT_HIGHLIGHT ):
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
                    # Sort the rectangles of this single annotation according to the reading flow
                    highlight_coords = sort_rectangles( highlight_coords )
                # Append an annotation object containing the annotation, the coords and the number of rectangles
                annot_cleaned_list.append( annot_cleaned(annot, highlight_coords, n_rects) )
            # For the text and freeplane output, we consider all  annotation types that may contain data/information/content
            elif ( output_mode == "h2a_txt" or output_mode == "h2a_freeplane" ):
                if ( annot.type[0] == fitz.PDF_ANNOT_TEXT or annot.type[0] == fitz.PDF_ANNOT_FREE_TEXT ): # pop-up annotation or free-text
                    # Create a dummy array for the coordinates
                    highlight_coords = [0, 0, 0, 0]
                    # Set number of rectangles to 0 to indicate a non-highlight annotation (no need to extract highlighted text for this one)
                    n_rects = 0
                    annot_cleaned_list.append( annot_cleaned(annot, highlight_coords, n_rects) )
                
        # Retrieve all words on this page including their coordinates
        all_words_on_page = page.get_text('words', delimiters=delimiters_to_detect_words_in_PDF)
        
        # Loop over all annotations of this page
        # @note We could combine the loop above and this one, but to keep it cleaner and easier to follow, we use separate loops.
        for annot_i in annot_cleaned_list:
            # If the creation date is empty/missing ...
            if ( len(annot_i.annotation.info['creationDate'])==0 ):
                # ... we write the modification date into this spot to ensure that creationDate is non-empty.
                # The creationDate is important to detect a "new" annotation. However, if the creationDate is yet empty,
                #  this means we have not yet processed this annotation anyway, so it is clearly new and more recent than
                #  the last h2a-run (see details in annot_toBe_changed_time(*))
                if ( len(annot_i.annotation.info['modDate'])==0 ):
                    annot_i.annotation.set_info( modDate=time_current )
                annot_modDate = annot_i.annotation.info['modDate']
                annot_i.annotation.set_info( creationDate=annot_modDate )
            # If the annotation misses an ID, we recreate it with an automatically created ID
            # @note The automatically created ID is only page-unique and not unique throughout the PDF
            if ( len(annot_i.annotation.info['id'])==0 ):
                print("h2a_highlightedText_to_annotation<< Found annotation without ID. Recreating it with new ID.")
                annot_text_tmp = annot_i.annotation.info['content']
                annot_modDate_tmp = annot_i.annotation.info['modDate']
                annot_creationDate_tmp = annot_i.annotation.info['creationDate']
                annot_title_tmp = annot_i.annotation.info['title']
                page.delete_annot( annot_i.annotation )
                annot_i.annotation = page.add_highlight_annot( quads=annot_i.coords )
                annot_i.annotation.set_info( content=annot_text_tmp, creationDate=annot_creationDate_tmp, modDate=annot_modDate_tmp, title=annot_title_tmp )
            # First check whether the annotation is to be changed based on the update_procedure, the creation date, and the modification date            
            if annot_toBe_changed_time( annot_i.annotation, time_current, H2A_protocol, output_mode, update_procedure ):
                # n_rects > 0 means we process a highlight annotation which contains rectangles that need to be used to extract the text
                if ( annot_i.n_rects > 0 ):
                    highlight_text = []
                    # Loop over all rectangles that belong to this annotation
                    # (adding all highlighted words of this annotation into a string that is written into the annotation content)
                    for i_rect in range(0,annot_i.n_rects):
                        # @todo-clean How to merge these two cases, maybe save the coordinates nicer or call a method on each annotation
                        if annot_i.n_rects == 1:
                            h_rect = annot_i.coords
                        else:
                            h_rect = annot_i.coords[i_rect][0:4]
                        # Assign the x,y and min,max coordinates of the bounding box for this highlighted rectangle
                        xmin_h, ymin_h, xmax_h, ymax_h = h_rect[0], h_rect[1], h_rect[2], h_rect[3]
                        # Loop over all words on this page to find words that cover the rectangle of the highlight
                        # @note We could use highlighted_word = page.get_textbox( h_rect ), but this is currently (pymupdf v1.23.5) not reliable
                        # @todo "page.get_text( 'text', clip=h_rect, textpage=text_page )" seems to work better, test it
                        for w in all_words_on_page:
                            # Retrieve the word as text
                            # @todo Improve encoding to be able to read more symbols and special characters
                            current_word = w[4]
                            # Assign the x,y and min,max coordinates of the current word
                            xmin_w, ymin_w, xmax_w, ymax_w = w[0],w[1],w[2],w[3]
                            # Compute the coverage to see whether the current word lies within the highlight bounding box
                            coverage = containment_of_a_in_b( xmin_w, ymin_w, xmax_w, ymax_w, xmin_h, ymin_h, xmax_h, ymax_h )
                            # If the current word lies by 30% in the highlight
                            # and it is in the same line, we see this as "contained" -> the current_word is highlighted
                            if ( coverage > 0.3 and is_on_same_line( fitz.Rect(w[0:4]), fitz.Rect(h_rect[0:4]) ) ):
                                highlighted_word = current_word
                                # Debugging
                                #highlighted_word = highlighted_word + '_' + str(round(coverage,2))
                                # Append the current word to a list of yet not connected words
                                highlight_text.append(highlighted_word)
                    # Join the words in the highlight_text for the current annotation by spaces
                    # Details: [https://pymupdf.readthedocs.io/en/latest/annot.html#Annot.info]
                    # @todo When a word is split over multiple lines like "splitting" as "split-\nting", we can remove the hyphen, but e.g. not for "FEM-method"
                    #       So how to decide this?
                    highlighted_phrase = " ".join(highlight_text)
                    # Remove leading and trailing punctuation marks that are usually undesired
                    if ( len(highlighted_phrase)>=1 and highlighted_phrase[0] in list_of_punctuationMarks_that_are_removed_if_leadingTrailing ):
                        highlighted_phrase = highlighted_phrase[1:]
                    if ( len(highlighted_phrase)>=1 and highlighted_phrase[-1] in list_of_punctuationMarks_that_are_removed_if_leadingTrailing ):
                        highlighted_phrase = highlighted_phrase[:-1]
                    # If the first character is the equal sign "=" add an apostrophe to avoid Freeplane trying to detect this node as formula (start with equal sign)
                    if ( len(highlighted_phrase)>=1 and highlighted_phrase[0] == "=" ):
                        highlighted_phrase = "'" + highlighted_phrase
                    # If the update procedure states to remove the comment text, we do not read the current comment_text, thus overwriting it by ""
                    if ( update_procedure == "update_all_removeCommentText" ):
                        comment_text = ""
                    # Extract existing comment part (stored after autoMarker e.g.' >a> ') from the annotation content
                    # (look inside the function, it's not trivial)
                    else:
                        comment_text = extract_comment_text( annot_i.annotation, H2A_protocol, title_suffix, autoMarker )
                    # Build new content of annotation from detected highlighted text and existing comment_text
                    if ( len(comment_text)==0 ):
                        output_content = highlighted_phrase
                    else:
                        output_content = highlighted_phrase + autoMarker + comment_text
                    # Depending on the output_mode, update the annotation and/or output the text
                    # For output_mode h2a and h2a_annot, we update the annotation with the content, the modification date, and the title
                    if ( output_mode in {'h2a','h2a_annot'} ):
                        # Add the title_suffix to the title of the annotation to declare it as being modified by h2a
                        new_title = get_new_title( annot_i.annotation, title_suffix )
                        # The text content of the current annotation annot_i is replaced by
                        # the detected highlighted text with the autoMarker followed by the existing text
                        annot_i.annotation.set_info( content=output_content, modDate=time_current, title=new_title )
                    # For output_mode h2a_txt, the highlighted text should only be output to a text-file, so no modification of the annotations
                    elif ( output_mode == 'h2a_txt' ):
                        f.write(output_content+'\n')
                    # For output_mode h2a_freeplane, we update the pdf as usual, 
                    # but also output the annotation to the special pdf-output file for Freeplane
                    elif ( output_mode == 'h2a_freeplane' ):
                        # Also process the the annot set_info as above to keep the annot up to date
                        # @todo maybe merge the first part here with the above h2a (duplicate code)
                        new_title = get_new_title( annot_i.annotation, title_suffix )
                        annot_i.annotation.set_info( content=output_content, modDate=time_current, title=new_title )
                        # Output the detected highlighted text to the output file
                        # @todo Centralise the output in a separate function to control it in a single  place
                        f.write( output_content.replace('\n',line_break_replacer).replace('\r',line_break_replacer) + ES
                                 + "highlight" + ES + str(page.number+1) + ES
                                 + annot_i.annotation.info['id']  + ES + time_current + ES + '\n' )
                # n_rects = 0 means we process a pop-up note annotation, where there is no highlight text to be extracted, 
                #             but only the existing content to be output
                elif ( annot_i.n_rects == 0 ):
                    # Modification for a pop-up note can only come from Freeplane, so we only do something here for h2a_freeplane output_mode
                    if ( output_mode == 'h2a_freeplane' ):
                        # Also process the annot set_info as above to keep the annot up to date
                        new_title = get_new_title( annot_i.annotation, title_suffix )
                        # Do not reset the content, but only the modification time
                        annot_i.annotation.set_info( modDate=time_current, title=new_title )
                        # Replace line breaks ("\n" and also carriage return "\r", the latter seems to occur for an empty line) by the line_break_replacer
                        annot_content = annot_i.annotation.info['content'].replace('\n',line_break_replacer).replace('\r',line_break_replacer)
                        # If the first character is the equal sign "=" add an apostrophe to avoid Freeplane trying to detect this node as formula (start with equal sign)
                        if ( len(annot_content)>=1 and annot_content[0] == "=" ):
                            annot_content = "'" + annot_content
                        # Output the note content to the output file
                        f.write( annot_content + ES
                                 + "note" + ES + str(page.number+1) + ES
                                 + annot_i.annotation.info['id']  + ES + time_current + ES + '\n' )
                annot_counter += 1
            # For the h2a_freeplane output_mode, we need to output all annotation even ones that did not change in the pdf ot keep Freeplane up to date
            elif ( output_mode == 'h2a_freeplane' ):
                # We do not extract the highlighted text, but only take the existing content and output it
                annot_content = annot_i.annotation.info['content'].replace('\n',line_break_replacer).replace('\r',line_break_replacer)
                annot_time = annot_i.annotation.info['modDate'] # Keep the old time
                # if the modification date is empty
                if ( len(annot_time)==0 ):
                    # we write the creation date into this spot
                    annot_time = annot_i.annotation.info['creationDate']
                #annot_time = get_datetime_from_pdftime( annot_time )
                #annot_time = annot_time.strftime("D:%Y%m%d%H%M%S%z")
                #annot_time = annot_time[0:16]+"+01'00"
                if ( annot_i.n_rects > 0 ):
                    annot_type = "highlight"
                else:
                    annot_type = "text"

                f.write( annot_content + ES
                         + annot_type + ES + str(page.number+1) + ES
                         + annot_i.annotation.info['id']  + ES + annot_time + ES + '\n' )
            
    time_processing = time.process_time() - tic
    print("h2a_highlightedText_to_annotation<< ... finished processing the pages in "+str(round(time_processing,2))+".")
    
    
    ## Process H2A protocol
    process_H2A_protocol( annot_counter, time_current, time_processing, doc[0], h2a_version )
    
    
    ## Save output
    if ( output_mode == 'h2a_txt' ):
        f.close()
    elif ( output_mode == 'h2a_freeplane' ):
        doc.saveIncr()
        f.close()
    # Save the pdf with the modified annotations into the input_file, thereby overwriting it
    elif ( output_mode == 'h2a' ):
        doc.saveIncr()
    # Save the pdf with the modified annotations into a separate output_file
    elif ( output_mode == 'h2a_annot' ):
        output_file = get_output_file_annot( input_file )
        doc.save(output_file)
    

    ## Update h2a-logfile
    update_h2a_logfile( time_current, pdf_name, h2a_version, annot_counter, n_pages, time_processing, path_to_tmp_directory )    
