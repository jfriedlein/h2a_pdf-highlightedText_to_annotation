import datetime
#import pytz
def get_datetime_from_pdftime( pdf_time, annot=0 ):
    # juggle between different date formats
    if ( "'" in pdf_time ): # timezone information is given
        #return datetime.datetime.strptime(pdf_time.replace("'", ""), "D:%Y%m%d%H%M%S%z").astimezone(pytz.timezone('Europe/Berlin')).strftime("D:%Y%m%d%H%M%S%z")
        return datetime.datetime.strptime(pdf_time.replace("'", ""), "D:%Y%m%d%H%M%S%z").replace(tzinfo=None)
    else: # no timezone information is given
        print( "get_datetime_from_pdftime<< Missing timezone in pdf_time="+pdf_time )
        # This is only attempting a bugfix of older okular versions, this block should normally not be called
        # @todo Currently we assume the local time zone is "+1", so we add one hour
        return datetime.datetime.strptime(pdf_time, "D:%Y%m%d%H%M%S") + datetime.timedelta(hours=1)
