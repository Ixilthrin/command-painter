command-painter
===============

Qt GUI Generator for Command Painting

You are creating a simple GUI that will generate a command.

First create an input file.  The language is simple.  Each line represents a keyword or text.  The keywords are:

title - The following line becomes the title of the GUI dialog.

literal  - whatever is on the next line becomes part of the command as is.

option - The following line is the name of the option, the following line after that becomes part of the command when selected.

choice - The following line is the name of the group, after that is the name of the choice, after that is the text for the command.

textbox - The following line is the label.  Any text entered by the user becomes part of the command.


The input file is piped to the generator, and the output is a GUI dialog written in Python.

Redirect the output to a file, and execute the file using Python.

Any change in the dialog or any click on the dialog automatically copies the command to the clipboard.

Just paste into a terminal and you have painted your command.


Here is an example of an input file for generating a find command piped to grep:

title
Find in Files
literal
find -name 
textbox
File
| xargs grep  
option
Ignore Case
-i
option
Line Numbers
-n
textbox
Search String
option
Auto Run
\n


Run this to generate the GUI:

cat input_file_name | python gen_widget.py > widget.py

Run the widget:

python widget.py
