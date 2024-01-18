from h2a_functions.is_on_same_line import is_on_same_line

def sort_rectangles ( list_of_rectangles ):
    # Sort the rectangles top to bottom
    # The coordinate origin appears to be in the top-left corner
    line_i = [0] * len(list_of_rectangles)
    sorted_list_of_rects = []
    for i_line in range(1,12):
        # Retrieve list of ymin coordinates of unassigned rectangles
        # [https://stackoverflow.com/questions/2739800/extract-list-of-attributes-from-list-of-objects-in-python]
        list_unassigned_rects = []
        index_map = []
        for i, rect in enumerate(list_of_rectangles):
            if line_i[i] == 0:
                list_unassigned_rects.append(rect)
                index_map.append(i)
            
        # If all elements have been sorted (list of unassigned elements is zero) ...
        if ( len(list_unassigned_rects)==0 ):
            break # ... end the line sorting loop
            
        # Collect the y-coordinates of the rectangle's tops
        list_ytop = [o.y1 for o in list_unassigned_rects]
        
        # Find rectangle with min ytop
        indexU_ymin = list_ytop.index(min(list_ytop))
        index_ymin = index_map[indexU_ymin]
        line_i[index_ymin] = i_line
        # Loop over all rectangles excluding the top most one
        for i, rect in enumerate(list_of_rectangles):
            if ( i != index_ymin and (rect in list_unassigned_rects) ):
                # Check whether the current rectangle rect is on the same line as the reference one
                if is_on_same_line( rect, list_of_rectangles[index_ymin] ):
                    # If rect is on the same line, assign the same line number
                    line_i[i] = i_line
        
        # @STATE Rectangles for current line i_line are complete
        
        # Sort the rectangles left to right by xmin
        li = []
        # Extract a sublist with all rectangles for the current line i_line
        # @todo This could be easily done with numpy, Pandas and Co.
        for i, rect in enumerate(list_of_rectangles):
            if ( line_i[i] == i_line ):
                li.append([list_of_rectangles[i].x0,i])
        # Sort the sublist according to the xmin coordinate of each rectangle
        li.sort()
        # Enter the sorted rectangles for the current line into the output
        for x in li:
            sorted_list_of_rects.append( list_of_rectangles[x[1]] )
        
        # Abort if the loop seems to run forever
        if ( i_line==11 ):
            print("sort_rectangles<< Reached line number 9")
            
    return sorted_list_of_rects