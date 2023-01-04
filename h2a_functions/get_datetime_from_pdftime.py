import datetime
#import pytz
def get_datetime_from_pdftime( pdf_time ):
    # juggle between different date formats
    if ( "'" in pdf_time ):
        #return datetime.datetime.strptime(pdf_time.replace("'", ""), "D:%Y%m%d%H%M%S%z").astimezone(pytz.timezone('Europe/Berlin')).strftime("D:%Y%m%d%H%M%S%z")
        return datetime.datetime.strptime(pdf_time.replace("'", ""), "D:%Y%m%d%H%M%S%z").replace(tzinfo=None)
    else:
        return datetime.datetime.strptime(pdf_time, "D:%Y%m%d%H%M%S")#.astimezone(pytz.timezone('Europe/Berlin')).strftime("D:%Y%m%d%H%M%S%z")
