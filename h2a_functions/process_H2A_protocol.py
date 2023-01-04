## Process H2A protocol
def process_H2A_protocol( annot_counter, time_current, time_processing, first_page, h2a_version ):
    # Retrieve data
    annot_counter_str = str(annot_counter)
    time_processing_str = str(round(time_processing,2))
    # Read possibly existing H2A protocol
    protocol_found = False
    # Loop over all annotations of the first page
    # @todo use retrieve_H2A_protocol function
    for annot in first_page.annots():
        # If the annotation content contains the catch phrase, we have found the protocol
        if ( 'H2A-protocol' in annot.info['content'] ):
            protocol_found = True
            # Retrieve old protocol
            protocol_content_old = list( annot.info['content'].split("\n") )
            
            # Update protocal with new data
            protocol_content_new=[]
            # H2A-protocol:
            protocol_content_new.append( protocol_content_old[0] )
            # h2a-version:
            protocol_content_new.append( protocol_content_old[1]+h2a_version+'; ' )
            # log:
            protocol_content_new.append( protocol_content_old[2]+time_current+'; ' )
            # number of processed annot:
            protocol_content_new.append( protocol_content_old[3]+annot_counter_str+'; ' )
            # processing time (s):
            protocol_content_new.append( protocol_content_old[4]+time_processing_str+'; ' )
            # n_errors (manual):
            protocol_content_new.append( protocol_content_old[5]+'-'+'; ' )
            
            # update protocol annnotation text
            annot.set_info( content="\n".join(protocol_content_new) )
    
            break # Leave the loop after the protocol was found
    
    # Create new H2A-protocol, if no old protocol exists
    if ( protocol_found==False ):
        # create protocol
        protocol_content =  'H2A-protocol:\n' +\
                            '- h2a-version: '+h2a_version+'; \n' +\
                            '- log: '+time_current+'; \n' +\
                            '- number of processed annot: '+annot_counter_str+'; \n' +\
                            '- processing time (s): '+time_processing_str+'; \n' +\
                            '- n_errors (manual): -; '
        first_page.add_text_annot( text=protocol_content, point=(10,10) )
