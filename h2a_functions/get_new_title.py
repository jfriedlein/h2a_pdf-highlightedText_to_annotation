def get_new_title ( annot, title_suffix ):
    # Add the title_suffix to the title if it is not already there
    old_title = annot.info['title'] 
    if ( title_suffix not in old_title ):
        return old_title + title_suffix
    else:
        return old_title