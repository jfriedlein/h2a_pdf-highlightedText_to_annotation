# Create a GUI to execute h2a and show info for PDF, both is activated by drag&drop of PDF files

# Clean the workspace and the console for a fresh start as in Matlab "clear,clc"
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

# Import tkinter and tkinterdnd2 for python GUI
import tkinter as tk
import tkinterdnd2
# Import os for working with paths
import os
# Import fitz to get first pdf page and annotations for pdf info
import fitz
# Import h2a commander to execute h2a
from h2a_commander import h2a_commander
# Import sys to load h2a functions from subfoldder
import sys
sys.path.append('./h2a_functions')
# Import retrieve_H2A_protocol to show the pdf info
from retrieve_H2A_protocol import retrieve_H2A_protocol
from get_output_file_annot import get_output_file_annot
from check_input_filename import check_input_filename
from h2a_unddo import h2a_unddo

# execute h2a on given path_file triggered on drag&drop
# [https://stackoverflow.com/questions/71890577/tkinterdnd2-drag-and-drop-not-firing-drop-event]
def dropexe(event):
    # remove curly parentheses
    path_file = event.data[1:-1]
    # execute h2a on path_file
    exe_h2a( path_file )
    
# execute h2a and update the GUI
def exe_h2a( path_file ):
    # reset exe listbox
    lb_exe.configure(background='white')
    lb_exe.delete(0,tk.END)
    
    # First ensure that the given file is indeed a pdf
    if ( check_input_filename( path_file )==False ):
        print("exe_h2a<< Error provided file is not a PDF.")
        tk.messagebox.showerror("exe_h2a", "Error: Provided file is not a PDF.")
        lb_exe.configure(background="red")
        return False
    
    # Split into path and filename
    path = os.path.split(path_file)[0]
    filename = os.path.split(path_file)[1]
    
    # Set the exe button
    button_exe['text'] = path_file
    button_exe["state"] = "normal"

    # Enter some infos into the exe listbox
    lb_exe.insert(0, "Execute h2a (drag&drop PDF file here)")
    lb_exe.insert(1, "path: "+path)
    lb_exe.insert(2, "file: "+filename)
    
    # Retrieve the settings for h2a from the drop down menus and text box
    output_mode = output_mode_clicked.get()
    update_procedure = update_proc_clicked.get()
    autoMarker = text_box_marker.get(1.0, "end-1c")
    
    # Run h2a on path_file with the given settings
    h2a_commander( path_file, output_mode, update_procedure, autoMarker )
    
    # after execution, change listbox to green
    lb_exe.configure(background="green")
    
    # after execution, update the info box
    if ( output_mode=='h2a_annot' ):
        # When outputting to a new file, we want to show the pdf info for the new file
        output_file = get_output_file_annot( path_file )
        output_info( output_file )
    else:
        output_info( path_file )

# show pdf infos triggered on drag&drop
def drop_info(event):
    # remove curly parentheses to get proper path
    path_file = event.data[1:-1]
    
    # First ensure that the given file is indeed a pdf
    if ( check_input_filename( path_file ) ):
        # output the info
        output_info( path_file )
    # If it is not a pdf, output error message
    else:
        print("drop_info<< Error provided file is not a PDF.")
        tk.messagebox.showerror("drop_info", "Error: Provided file is not a PDF.")
        lb_info.configure(background="red")
        return False
    
    button_open_info_pdf["state"] = "normal"
    button_unddo_info_pdf["state"] = "normal"
    
# output pdf info into list box
def output_info( path_file ):
    # reset info listbox
    lb_info.delete(0,tk.END)
    lb_info.configure(background='white')
    
    # Set the info exe button
    button_info_exe['text'] = path_file
    button_info_exe["state"] = "normal"
    
    # Split into path and filename
    path = os.path.split(path_file)[0]
    file = os.path.split(path_file)[1]
    
    # Open the pdf into "doc"
    doc = fitz.open( path_file )
    
    # number of pages
    n_pages = len(doc)
    
    # Enter some info into the info listbox
    lb_info.insert(0, "Output file info (drag&drop PDF file here)")
    lb_info.insert(1, "path: "+path)
    lb_info.insert(2, "file: "+file)
    lb_info.insert(3, "n pages: "+str(n_pages))
    #lb_info.insert(4, "n annot: "+str(n_annots))
    #lb_info.insert(5, "n high: "+str(n_highlights))

    # Read H2A protocol and output to listbox
    H2A_protocol = retrieve_H2A_protocol( doc[0] )
    for i,line_i in enumerate(H2A_protocol):
        lb_info.insert(4+i, line_i )

# Create main window
window = tkinterdnd2.Tk()
window.title('h2a - pdf highlighted text to annotation')

# Create info list box
lb_info = tk.Listbox(window, width=110, height=14)
lb_info.drop_target_register(tkinterdnd2.DND_FILES)
lb_info.insert(0, "Output file info (drag&drop PDF file here)")
lb_info.dnd_bind("<<Drop>>", drop_info )
lb_info.pack(padx=2,pady=2,fill=tk.BOTH,expand=True)

# button to run h2a on file in info box
tk.Label(text='h2a:').place(x=60, y=180)  
def h2a_on_info():
    exe_h2a( button_info_exe['text'] )
button_info_exe=tk.Button(
   window, 
   text="h2a on file in info box",
   width=80,
   anchor="e",
   command=h2a_on_info
)
# The button is initially off and only activated after drag&drop of a proper pdf file
button_info_exe["state"] = "disabled"
button_info_exe.pack()

# Create button to open pdf file in info box with default pdf application
def open_pdf():
    os.system('xdg-open "'+button_info_exe['text']+'"')
button_open_info_pdf=tk.Button(
   window, 
   text="PDF",
   width=1,
   command=open_pdf
)
button_open_info_pdf["state"] = "disabled"
button_open_info_pdf.place(x=3,y=176)
##740

# Create button to unddo h2a on pdf file in info box
def unddo_h2a():
    path_file = button_info_exe['text']
    h2a_unddo( path_file )
    output_info( path_file )
button_unddo_info_pdf=tk.Button(
   window, 
   text="Unddo",
   width=3,
   command=unddo_h2a
)
button_unddo_info_pdf["state"] = "disabled"
button_unddo_info_pdf.place(x=720,y=176)

# Alter h2a settings
# Output mode
tk.Label(text='output mode').place(x=10, y=220)
# Create Dropdown menu
output_mode_options = [
    "h2a",
    "h2a_annot",
    "h2a_txt"
]
output_mode_clicked = tk.StringVar()
output_mode_clicked.set( output_mode_options[0] )
output_mode = tk.OptionMenu( window , output_mode_clicked, *output_mode_options )
output_mode.config(width = 8)
output_mode.pack(side=tk.LEFT)

# update procedure
tk.Label(text='update proc').place(x=120, y=220)
# Create Dropdown menu
update_proc_options = [
    "update_new",
    "update_auto",
    "update_all"
]
update_proc_clicked = tk.StringVar()
update_proc_clicked.set( update_proc_options[0] )
update_proc = tk.OptionMenu( window , update_proc_clicked, *update_proc_options )
update_proc.config(width = 10)
update_proc.pack(side=tk.LEFT)

# auto marker
tk.Label(text='auto marker').place(x=220, y=220)
# Create text box with custom input
text_box_marker = tk.Text(
    window,
    height=1,
    width=12
)
text_box_marker.config(state='normal')
text_box_marker.pack(side=tk.LEFT)

# Set/reset the values/settings of the drop down menus and text box
def reset_to_default_settings():
    text_box_marker.delete('1.0','end')
    text_box_marker.insert('end', ' >a> ')
    output_mode_clicked.set(output_mode_options[0])
    update_proc_clicked.set(update_proc_options[0])

# Set the initial values for the text boxes (initially only important for text box)
reset_to_default_settings()

# Create button to manually reset the settings
button_reset = tk.Button(
   window, 
   text="default settings", 
   command=reset_to_default_settings
)
button_reset.place(x=80, y=265)

# Create list box for h2a execution
lb_exe = tk.Listbox(window, width=64, height=5)
lb_exe.drop_target_register(tkinterdnd2.DND_FILES)
lb_exe.insert(0, "Execute h2a (drag&drop PDF file here)")
lb_exe.dnd_bind("<<Drop>>", dropexe)
lb_exe.pack(padx=2,pady=2,fill=tk.BOTH,expand=True)

# button to run h2a on file in exe box
tk.Label(text='h2a:').place(x=275, y=275)
def h2a_on_exe():
    exe_h2a( button_exe['text'] )
button_exe=tk.Button(
   window, 
   text="h2a on file in exe box",
   width=64,
   anchor="e",
   command=h2a_on_exe
)
# The button is initially off and only activated after drag&drop of a proper pdf file
button_exe["state"] = "disabled"
button_exe.pack()

window.mainloop()