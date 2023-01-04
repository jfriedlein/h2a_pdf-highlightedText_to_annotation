import os

def get_output_file_annot( input_file ):
    output_file = os.path.splitext(input_file)[0]+"_annot"+".pdf"
    return output_file