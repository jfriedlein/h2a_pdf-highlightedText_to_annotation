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
from h2a_functions.update_h2a_logfile import update_h2a_logfile

def h2a_update_from_freeplane ( path_file="./h2a_freeplane-changes.tmp" ):
    
    ## CODE
    # h2a-version
    h2a_version = 'V2.0'
    
    # Entry-separator "ES"
    # @todo This should be unified here in "h2a_highlightedText_to_annotation.py" and in the Freeplane groovy script
    ES = ' ;x; '
    
    # Open the tmp file to extract the path to the pdf from the first line
    with open( path_file, 'r') as f:
        first_line = f.readline().strip('\n')
        input_file = first_line.replace('%20',' ')
    
    # Get name of pdf (head of path)
    pdf_name = os.path.split(input_file)[1]
    
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
    with open( path_file, 'r') as f:
        # skip the first line (already read above for the pdf-file)
        next(f)
        
        for line in f:
            # Extract the information on the annotation from the line in the tmp-file
            line_split = line.split( ES )
            annot_content_fromFreeplane = line_split[0]
            annot_page = int(line_split[1]) - 1
            #annot_type = line_split[2]
            annot_ID = line_split[3]
            annot_modTimePDF = line_split[4]
            #modTimePDF_freeplaneChanges = annot_modTimePDF
            #annot_modTimeFreeplane = line_split[5]
            
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
                        annot.set_info( content=annot_content_fromFreeplane, modDate=annot_modTimePDF )
                        annot_counter += 1

    time_processing = time.process_time() - tic
    print("... finished processing the pages in "+str(round(time_processing,2))+".")
    
    if ( annot_counter > 0 ):
        # We should not add this run to the H2A-protocol, because this would declare these changes as "auto",
        #  but they come from manual changes in Freeplane, so they should be protected from overwriting
        #process_H2A_protocol( annot_counter, modTimePDF_freeplaneChanges, time_processing, doc[0], h2a_version )
    
        doc.saveIncr()
    
        ## Update h2a-logfile
        update_h2a_logfile( time_current, pdf_name, h2a_version, annot_counter, n_pages, time_processing )    
