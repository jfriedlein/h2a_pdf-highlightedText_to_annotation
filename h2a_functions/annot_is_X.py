# The annotation is protected if its content annot_text contains '>p>'
def annot_is_protected( annot_text ):
    return ( '>p>' in annot_text )

# The annotation is auto-created if its content annot_text contains '>a>'
def annot_is_autoCreated( annot_text ):
    return ( '>a>' in annot_text )