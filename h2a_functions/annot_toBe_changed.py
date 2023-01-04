from annot_is_X import annot_is_protected, annot_is_autoCreated

def annot_toBe_changed( annot_text, output_mode, update_procedure ):
    if ( update_procedure == 'update_all' or output_mode=='h2a_txt' ):
        return True
    elif ( update_procedure == 'update_auto' ):
        if annot_is_protected( annot_text ):
            return False
        elif annot_is_autoCreated( annot_text ):
            return True
        else:
            return True
    elif ( update_procedure == 'update_new' ):
        if annot_is_protected( annot_text ):
            return False
        elif annot_is_autoCreated( annot_text ):
            return False
        else:
            return True