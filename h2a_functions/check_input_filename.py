import os

# check that the given file 'path_file' is a pdf
def check_input_filename( path_file ):
    # if not a pdf, return false
    if ( os.path.splitext(path_file)[1]!=".pdf" ):
        return False
    else:
        return True