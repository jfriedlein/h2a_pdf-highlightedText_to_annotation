#import datetime
import re
from h2a_functions.get_datetime_from_pdftime import get_datetime_from_pdftime

def annot_toBe_changed_time( annot, time_current, H2A_protocol, output_mode, update_procedure ):
    # If ...
    #  ... the update prodecure states "update_all", or
    #  ... the output mode is h2a_txt, or
    #  ... there is no H2A-protocol, which means a yet unprocessed file
    # then this annotation is to be changed -> return True
    if ( update_procedure == 'update_all' or update_procedure == 'update_all_removeCommentText' or output_mode=='h2a_txt' or len(H2A_protocol) == 0 ):
        return True # ... to be processed

	# Else we need to check for creation and modification times
    # Read the creation date of the annotation (ensured that it is non-empty from h2a_highlightedText_to_annotation(*))
    creationDate = annot.info['creationDate']
    creaDate = get_datetime_from_pdftime( creationDate )

    # Extract the last h2a run from the H2A-protocol to get the time when h2a was last executed
    last_h2a_run = re.split(r' |; ',H2A_protocol[2])[-2]
    last_h2a_time = get_datetime_from_pdftime( last_h2a_run )

    # "update_new": Only process annotations which have been created since the last h2a run,
    #               because these are completely unprocessed yet so "new"
    if ( update_procedure == 'update_new' ):
        if ( creaDate > last_h2a_time ): # new annotation ...
            return True # ... to be processed
        else: # old annotation
            return False # ... not to be processed
    # "update_auto": Process only annotations which were automatically modified or are new ("new" as for above "update_new")
    elif ( update_procedure == 'update_auto' ):
        # When updating only automatically created entries, we want to keep specifically
        # the protected (manually chanaged entries) unchanged.
        # A manually changed entry is defined by a modification date different from any h2a-log time, 
        # because the user modified the annotation at a time, which does not equal a h2a run.
        # @todo-optimize If the reading of modDate creates errors, we know it was not created by h2a
        #modDate = get_datetime_from_pdftime( annot.info['modDate'] ).strftime("D:%Y%m%d%H%M%S%z")
        modDate = annot.info['modDate']
        # Extract the list of all previous h2a-runs
        list_of_h2a_runs = re.split(r' |; ',H2A_protocol[2])[2:-1]
        if ( (creaDate > last_h2a_time) # "new" annotation as for update_new
             or (modDate in list_of_h2a_runs) ): # by h2a automatically modified annotation
            return True # ... to be processed
        else: # neither a new nor a h2a-modified annotation
            return False # ... not to be processed