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
from h2a_functions.update_h2a_logfile import update_h2a_logfile

def h2a_update_from_freeplane ( tmp_pathFile="./h2a_freeplane-changes.tmp" ):
    
    ## CODE
    # h2a-version
    h2a_version = 'V2.0'
    
    # Entry-separator "ES"
    # @todo This should be unified here in "h2a_highlightedText_to_annotation.py" and in the Freeplane groovy script
    ES = ' ;x; '

    line_break_replacer = ' ;xnx; '
    
    h2a_metadata_entry = "h2a"
    
    # Open the tmp file to extract the path to the pdf from the first line
    # @note For some reason we cannot read the first line as with codecs.open and "utf-8", but this is also not needed for Linux. However, for Windows problems were observed when the path "input_File" contains e.g. "ü", so the encoding is set to utf-8 hoping to fix the issue
    # Using "replace" on errors during encoding [https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character]
    with open( tmp_pathFile, mode="r", encoding="utf-8", errors='replace' ) as f:
        first_line = f.readline().strip('\n')
        input_file = first_line.replace('%20',' ')

    # Get name of pdf (head of path)
    pdf_name = os.path.split(input_file)[1]
    
    # For the directory to the h2a-logfile extract the directory from the path to the h2a_Freeplane-changes tmp file
    path_to_tmp_directory = os.path.dirname(tmp_pathFile)
    
    # time_current is only used for the h2a-logfile (has no effect, pure output)
    time_current = datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime("D:%Y%m%d%H%M%S%z")
    time_current = time_current[0:19]+"'"+time_current[19:]

    print("Processing the pages of '"+pdf_name+"' ...")
    
    # Start timer to measure processing time
    tic = time.process_time()
    
    # Open the pdf into "doc"
    doc = fitz.open(input_file)
    
    # number of pages (for logfile)
    n_pages = len(doc)
    
    annot_counter = 0
    
    # Loop over each annotation that was changed in Freeplane
    # We read the file with utf-8 encoding using codecs to also get special characters [https://stackoverflow.com/questions/491921/unicode-utf-8-reading-and-writing-to-files-in-python]
    with codecs.open( tmp_pathFile, 'r', "utf-8") as f:
        # skip the first line (already read above for the pdf-file)
        next(f)
        
        for line in f:
            # Extract the information on the annotation from the line in the tmp-file
            line_split = line.split( ES )
            annot_content_fromFreeplane = line_split[0].replace(line_break_replacer,'\n')
            annot_page = int(line_split[1]) - 1
            #annot_type = line_split[2]
            annot_ID = line_split[3]
            annot_modTimePDF = line_split[4]
            #modTimePDF_freeplaneChanges = annot_modTimePDF
            #annot_modTimeFreeplane = line_split[5]
            
            # Extract the annotation colour
            # The annotation colour was added in h2aFreeplane-v2.1,
            #  hence it is not always included in tmp_pathFile and its existence is check via "len(line_split)"
            #  Moreover, its value can be empty if Freeplane does not provide a colour or uses the default colour, hence the "len(line_split[6])"-check
            annot_colour = []
            if ( len(line_split)>=6+2 and len(line_split[6])>0 ):
                # The colour is output in groovy e.g. as '[1.,1.,0]', 
                #  so we convert the string to a list using "eval" suitable for Python below
                annot_colour = eval(line_split[6])
            
            # Load the page where the annotation is located
            page = doc.load_page(annot_page)

            # Loop over all annotations on this page to find the changed one
            for annot in page.annots():
                if ( annot.info['id'] == annot_ID ):
                    # Check the modification time of the annotation, only update the pdf if freeplane contains newer changes
                    annot_modDate = annot.info['modDate']
                    # If the annotation has been changed in the PDF since loading it into Freeplane and we consider 
                    # the annotation here, which means that it was also changed in Freeplane since loading it from the PDF, 
                    # we have two changes
                    # This string comparison might work, but is anyway very dodgy 
                    if ( annot_modDate > annot_modTimePDF ):
                        # @todo how to decide what to do -> use newest, keep old, merge
                        # This should be solved in the Freeplane groovy script
                        print( "h2a_update_from_freeplane<< The annotation changed in the PDF and in Freeplane. Which one to take?\n" )
                        sys.exit(1)
                    else:
                        # @note It appears that it is not possible to set "content" to an empty string "",
                        #        so we set it to blankspace " ", it case the string is empty
                        if ( len(annot_content_fromFreeplane)<=0 ):
                            annot_content_fromFreeplane = ' '
                        annot.set_info( content=annot_content_fromFreeplane, modDate=annot_modTimePDF )
                        # If the annot_colour is active, we apply it as stroke colour
                        # @note We do not reset the annotation colour if Freeplane does not provide
                        #  a colour or wants to reset it to default, because I don't know how to reset
                        #  the pdf annotation to a/the default colour.
                        if ( len(annot_colour)>0 ):
                            annot.set_colors( stroke=annot_colour )
                        annot_counter += 1

    time_processing = time.process_time() - tic
    print("... finished processing the pages in "+str(round(time_processing,2))+".")
    
    # We should not add this run to the H2A-protocol, because this would declare these changes as "auto",
    #  but they come from manual changes in Freeplane, so they should be protected from overwriting
    #process_H2A_protocol( annot_counter, modTimePDF_freeplaneChanges, time_processing, doc[0], h2a_version )

    # Write a keyword into the metadata of the pdf to mark/tag it as having been processed by h2a
    # Extract the initial metadata
    pdf_metadata = doc.metadata
    # Ensure that the "keywords" key exists
    if ( 'keywords' in pdf_metadata ):
        # Extract the current keywords
        current_keywords = pdf_metadata['keywords']
        # If no keywords already exists ...
        if ( len(current_keywords)==0 ):
            # ... write the h2a keyword into the key
            doc.set_metadata({"keywords": h2a_metadata_entry})
        # If keywords already exist ...
        elif ( h2a_metadata_entry not in current_keywords ):
            # ... add the h2a key to the list of keywords, comma separated [https://stackoverflow.com/questions/44608608/the-separator-between-keywords-in-pdf-meta-data]
            doc.set_metadata({"keywords": current_keywords+", "+h2a_metadata_entry})

    doc.saveIncr()

    ## Update h2a-logfile
    update_h2a_logfile( time_current, pdf_name, h2a_version, annot_counter, n_pages, time_processing, path_to_tmp_directory )    
