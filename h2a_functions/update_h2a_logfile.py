# Import "os" for splitting the path with the operator specific file separator
import os

## Update h2a-logfile
def update_h2a_logfile( time_current, pdf_name, h2a_version, annot_counter, n_pages, time_processing, path_to_tmp_directory ):
    logfile_name = path_to_tmp_directory + os.sep + 'h2a-logfile.txt'
    # Check whether logfile already exists, if not then create it
    if not os.path.exists(logfile_name):
        with open(logfile_name, 'a') as logfile:
            logfile.write('Current time , PDF filename , h2a-version , nbr processed annotations , nbr pages , processing time\n')
    
    # Collect the relevant information and output it
    with open(logfile_name, 'a') as logfile: # create new file or append old
        log_data = [time_current, pdf_name, h2a_version, str(annot_counter), str(n_pages), str(round(time_processing,2))]
        logfile.write( " , ".join(log_data) + '\n' )
