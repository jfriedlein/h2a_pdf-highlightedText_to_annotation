# h2a_pdf-highlightedText_to_annotation
Python tool to extract highlighted text from a pdf file and write this text into content of each annotation

## What it does
This is a Python tool that reads a pdf page-by-page extracting the highlighted text and saves the highlighted words into the content field of the highlight annotation. This is ideally suited for Docear to prepare pdfs. Alternatively, he output mode "h2a_txt" enables to store the extracted highlight text to a separate txt file.

## Installation
for h2a: 
pip install fitz, ...

@todo Collect all necessary packages

for GUI:
pip install tkinter, ...

## Usability
### GUI
Start the GUI by calling "python h2a_GUI.py" and process the pdfs by drag&drop.

### command line
Process a pdf from the command line via the h2a_commander

### Python scripting
Create a python script that e.g. executes h2a on all pdfs in a folder.

## Settings
output_mode, update procedure, autoMarker

## Features
- text sorting: annotations that contain multiple rectangle of highlighted text are sorted according to the reading flow
- highlighted text detection: highlighted text in pdf files does not store the actual text, but the coordinates of the coloured rectangles. h2a detects which words are highlighted based on the area that a word of the pdf lies within the coloured rectangle and by checking that the word lies on the same line as the rectangle
- H2A protocol: h2a creates a protocal that is entered in the pdf by a note annotation on the first page. This protocol stores all executions of h2a and enables infinite runs of h2a on the same file without doing any harm.
- update procedures: modifying the content of the annotation after extraction is easily possible. Choosing the update procedure "update_new" or "update_all" will automatically detect such manually changed annotations and won't alter them. ("update_all" reprocesses all annotations)
- comment text: If the content of the highlight annotation already contains some text, the extracted highlight text is appended to existing text as "[extracted highlight text] >a> [already existing comment text]". Here " >a> " can be specified by the user as the "autoMarker".

## todo
- hyphen or no hyphen
- drag&drop of folder with pdfs
- top to bottom for h2a_txt
- what happens if an annotation spans two pages?
