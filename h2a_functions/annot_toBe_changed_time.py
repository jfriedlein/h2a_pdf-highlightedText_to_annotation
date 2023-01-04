#import datetime
import re
from get_datetime_from_pdftime import get_datetime_from_pdftime

def annot_toBe_changed_time( annot, time_current, H2A_protocol, output_mode, update_procedure ):
    # no protocol yet means yet unprocessed file
    if ( update_procedure == 'update_all' or output_mode=='h2a_txt' or  len(H2A_protocol) == 0 ):
        return True
    
    creationDate = annot.info['creationDate']
    # if the creation date is empty
    if ( len(creationDate)==0 ):
        # we write the modification date into this spot
        creationDate = annot.info['modDate']
        creaDate = get_datetime_from_pdftime( creationDate )
        # however with some modification of the time (timezone garbage)
        #creaDate += datetime.timedelta(hours=1)
        annot.set_info(creationDate=creaDate.strftime("D:%Y%m%d%H%M%S%z"))
    else:
        creaDate = get_datetime_from_pdftime( creationDate )
        
    last_h2a_run = re.split(r' |; ',H2A_protocol[2])[-2]
    last_h2a_time = get_datetime_from_pdftime( last_h2a_run )
    
    if ( update_procedure == 'update_new' ):
        if ( creaDate > last_h2a_time ):
            return True
        else:
            return False
    elif ( update_procedure == 'update_auto' ):
        # When updating only automatically created entries, we want to keep specifically the protected (manually chanaged entries)
        # A manually changed entry is defined by a modification date different from any h2a-log time
        # @todo-optimize If the reading of modDate creates errors, we know it was not created by h2a
        modDate = get_datetime_from_pdftime( annot.info['modDate'] ).strftime("D:%Y%m%d%H%M%S%z")
        list_of_h2a_runs = re.split(r' |; ',H2A_protocol[2])[2:-1]
        
        if ( (creaDate > last_h2a_time) or (modDate in list_of_h2a_runs) ):
            return True
        else:
            return False