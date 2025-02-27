def get_annot_colour( annot ):
    # Extract the stroke colour of the annotation and convert it to a string to export
    # @todo Does the "fill" colour matter and when?
    annot_colour = str(annot.colors['stroke'])
    return annot_colour