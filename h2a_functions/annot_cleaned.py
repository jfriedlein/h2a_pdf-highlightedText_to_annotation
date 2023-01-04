# Class to store the annotation together with the coordinates of all bounding rectangles and the number of rectangles
# @todo Clean-up, maybe we can just create a method inside this class that return the highlight coordinates directly
class annot_cleaned:
    annotation=[]
    coords = []
    n_rects=0
    # class constructor
    def __init__(self,annot,coord,n_rects): 
       self.annotation = annot
       self.coords=coord
       self.n_rects=n_rects