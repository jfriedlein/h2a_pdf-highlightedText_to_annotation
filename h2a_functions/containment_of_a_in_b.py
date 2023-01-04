# Define a function to compute how much of a rectangle "a" lies within a rectangle "b"
# Returns a ratio that is 1 if the entire area of "a" lies within "b", and 0 if "a" and "b" do not intersect
# Based on [https://stackoverflow.com/questions/9324339/how-much-do-two-rectangles-overlap]
def containment_of_a_in_b (xmin_a, ymin_a, xmax_a, ymax_a, xmin_b, ymin_b, xmax_b, ymax_b):
    intersecting_area = max(0, min(xmax_b, xmax_a)- max(xmin_b, xmin_a)) * max(0, min(ymax_b, ymax_a) - max(ymin_b, ymin_a) )
    area_a = (xmax_a-xmin_a)*(ymax_a-ymin_a)
    containment_ratio = intersecting_area / area_a
    return containment_ratio