## Process H2A protocol
def retrieve_H2A_protocol( first_page ):
    # Read possibly existing H2A protocol
    protocol_found = False
    # Loop over all annotations of the first page
    for annot in first_page.annots():
        # If the annotation content contains the catch phrase, we have found the protocol
        if ( 'H2A-protocol' in annot.info['content'] ):
            protocol_found = True
            # Retrieve old protocol
            protocol_content_old = list( annot.info['content'].split("\n") )
            break
    if ( protocol_found ):
        return protocol_content_old
    else:
        return []
            