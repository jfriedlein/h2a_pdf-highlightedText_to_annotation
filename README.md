# h2a_pdf-highlightedText_to_annotation
Python tool to extract highlighted text from a pdf file and write this text into content of each annotation

## What it does
This is a Python tool that reads a pdf page-by-page extracting the highlighted text and saves the highlighted words into the content field of the highlight annotation. This is ideally suited for Docear to prepare pdfs. Alternatively, the output mode "h2a_txt" enables to store the extracted highlight text to a separate txt file.

![h2a_scheme](https://github.com/jfriedlein/h2a_pdf-highlightedText_to_annotation/blob/main/guide/h2a_scheme.png)

## Installation
### Using executables
executables available for Windows and Linux (see "Releases"), no Python installation or packages required, but currently slow on startup)
### Using Python
Compatible with Linux and Windows (tested for Windows with python 3.11.1 custom installation based on ["Install Python under Windows"](https://www.digitalocean.com/community/tutorials/install-python-windows-10) already including tkinter)
To make sure you got all packages installed, I recommend starting the python file from the terminal, then you will see error messages.

@todo double check all necessary packages also for Linux

for h2a-algorithm: 
- pip install pymupdf (no need to directly install fitz, which may cause some problems)
- pip install pytz (for proper times and time zones)

for GUI:
- pip install tkinter
- pip install tkinterdnd2

## Features
- text sorting: annotations that contain multiple rectangle of highlighted text are sorted according to the reading flow
- highlighted text detection: highlighted text in pdf files does not store the actual text, but the coordinates of the coloured rectangles. h2a detects which words are highlighted based on the area that a word of the pdf lies within the coloured rectangle and by checking that the word lies on the same line as the rectangle
- H2A protocol: h2a creates a protocal that is entered in the pdf by a note annotation on the first page. This protocol stores all executions of h2a and enables infinite runs of h2a on the same file without doing any harm.
- update procedures: modifying the content of the annotation after extraction is easily possible. Choosing the update procedure "update_new" or "update_all" will automatically detect such manually changed annotations and won't alter them. ("update_all" reprocesses all annotations)
- comment text: If the content of the highlight annotation already contains some text, the extracted highlight text is appended to existing text as "[extracted highlight text] >a> [already existing comment text]". Here " >a> " can be specified by the user as the "autoMarker".
- dynamic: You can change your own annotations freely. If you change some of the automatically extracted text in the content field of the annotation, h2a detects such custom changes automatically (based on the annotation's last modified time) and protects the annotation when using the update procedure "update_auto". Never loose any data and keep working with the PDF.
- fast: Processing pdf with less than 100 pages takes a fraction of a second. Processing a book with 790 pages and 55 annotations takes around 1.4 seconds. If you look at the code, you might think all this looping over each word on the page takes forever, nope it is very very fast.

## Usability
Start with a PDF that contains for instance highlighted text and user-comments:
![pdf with comments after h2a](https://github.com/jfriedlein/h2a_pdf-highlightedText_to_annotation/blob/main/guide/pdf%20with%20comments%20before%20h2a.png)

### GUI
1. Start h2a GUI (python script h2a_GUI.py). Options:
- run executable available for Windows and Linux (see "Releases", no Python installation or packages required, but currently slow on startup)
- run vbs script (opens GUI directly)
- run batch script (opens command terminal, which shows possible error messages)
- open a terminal, change the directory "cd" to the folder with the h2a code, and start the GUI with "python h2a_GUI.py":
![Windows - start h2a_GUI from the terminal](https://github.com/jfriedlein/h2a_pdf-highlightedText_to_annotation/blob/main/guide/Windows%20-%20start%20h2a_GUI%20from%20the%20terminal.png)

2. Drag your PDF file into the "exe" box in the bottom right (note: PDF cannot be open in the very possessive Adobe Reader during h2a processing):
![Windows - h2a_GUI - drag&drop1](https://github.com/jfriedlein/h2a_pdf-highlightedText_to_annotation/blob/main/guide/Windows%20-%20h2a_GUI%20-%20drag%26drop1.png)

3. Drop it, which triggers the h2a-algorithm. Once the PDF is processed, the "exe" box turns green and information is shown in the "info" box at the top:
![Windows - h2a_GUI - drag&drop2 - exe](https://github.com/jfriedlein/h2a_pdf-highlightedText_to_annotation/blob/main/guide/Windows%20-%20h2a_GUI%20-%20drag%26drop2%20-%20exe.png)

Afterwards the PDF contains annotations with the extracted highlighted text and still contains all your user comments:
![pdf with comments after h2a](https://github.com/jfriedlein/h2a_pdf-highlightedText_to_annotation/blob/main/guide/pdf%20with%20comments%20after%20h2a.png)

### command line
Process a pdf from the command line via the h2a_commander

### Python scripting
Create a python script that e.g. executes h2a on all pdfs in a folder.

## Settings
output_mode, update procedure, autoMarker

@todo Add documentation on the settings

## Setup using vbs script
1. Download the entire repo
2. Create a desktop shortcut from the "h2a-GUI.vbs" script
3. Start the GUI by double clicking the desktop shortcut.

@todo extent setup

## todo
- hyphen or no hyphen
- drag&drop of folder with pdfs
- top to bottom for h2a_txt
- what happens if an annotation spans two pages?
