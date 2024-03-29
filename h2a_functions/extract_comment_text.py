# Import "re" for splitting strings with multiple delimiters [https://datagy.io/python-split-string-multiple-delimiters/]
import re
from h2a_functions.get_datetime_from_pdftime import get_datetime_from_pdftime

def extract_comment_text( annot, H2A_protocol, title_suffix, autoMarker ):
    # Extract the current content of this annotation
    annot_text = annot.info['content']
    # If the comment text contains an autoMarker (e.g. ' >a> '), it is clear how to split the text into extracted text and original comment text
    if ( autoMarker in annot_text ):
        # Extract the text after ([-1]) the marker (>a>) and remove possible leading whitespace (lstrip())
        return re.split(autoMarker,annot_text)[-1].lstrip()
    # Else the text is either a pure comment (without yet using h2a, so an empty H2A_protocal)
    elif ( len(H2A_protocol)==0 ):
        return annot_text
    # Or else it is a pure highlight text by using h2a without marker
    else:
        list_of_h2a_runs = re.split(r' |; ',H2A_protocol[2])[2:-1]
        #modDate = get_datetime_from_pdftime( annot.info['modDate'] ).strftime("D:%Y%m%d%H%M%S%z")
        modDate = annot.info['modDate']
        # Adding the title_suffix to the annotation is important to be able to
        # distinguish original comment text from manually modified extracted highlight text
        # @todo Rethink the following criteria, is this repetitive?
        if ( (modDate in list_of_h2a_runs) or (title_suffix in annot.info['title']) ):
            return ''
        else:
            return annot_text