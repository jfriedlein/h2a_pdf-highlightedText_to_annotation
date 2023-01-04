import fitz

# Input rect are of type fitz.Rect
def is_on_same_line( rect_i, rect_ref ):
    w_y_av = ( rect_i.y1 + rect_i.y0 ) /2.
    if ( w_y_av < rect_ref.y1 and w_y_av > rect_ref.y0 ):
        return True
    else:
        return False