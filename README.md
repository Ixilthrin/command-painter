command-painter
===============

<b> Qt GUI Generator for Command Painting

You are creating a simple GUI that will generate a command.

First create an input file.  The language is simple.  Each line represents a keyword or text.  The keywords are:

<b>title</b> - The following line becomes the title of the GUI dialog.

<b>literal</b>  - Whatever is on the next line becomes part of the command as is.

<b>option</b> - The following line is the name of the option, the following line after that becomes part of the command when selected.

<b>choice</b> - The following line is the name of the group, after that is the name of the choice, after that is the text for the command.  The text is added when the option is selected.  Choice entries with the same group name will become a radio button group in the dialog.

<b>textbox</b> - The following line is the label.  Any text entered by the user becomes part of the command.

<b>pasteselect</b> - Adds selection to command.  Linux only.

<b>pasteclip</b> - Adds clipboard text to command.


<b> Basic Description of Process for Creating a Widget

The input file is piped to the generator, and the output is a GUI dialog written in Python.

Redirect the output to a file, and execute the file using Python.

Any change in the dialog or any click on the dialog automatically copies the command to the clipboard.

Just paste into a terminal and you have painted your command.


The sample file input_find_in_files is provided that generates a find | grep command.


<b> Run this to generate the GUI:

cat input_find_in_files | python gen_widget.py > widget.py

<b>Run the widget:

python widget.py
