#!/usr/local/bin/python
import sys

class TextProvider:
    def __init__(self, guiNumber):
        self.guiNumber = guiNumber

    def getLabel(self):
        return self.label

    def getText(self):
        #return self.text.strip()
        return self.text

    def getInitializationCode(self):
        return ""

    def getType(self):
        return ""
   
    def getGuiNumber(self):
        return self.guiNumber

class Literal(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        self.text = addEscapeCharacters(lines[1])
        self.label = ""

    def getInitializationCode(self):
        return ""

    def getType(self):
        return "Literal"

# Supports deprecated keyword 'space'
class Space(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        self.label = ""
        self.text = " "

    def getInitializationCode(self):
        return ""

    def getType(self):
        return "Space"

    def getText(self):
        return self.text

# Support deprecated keyword 'quote'
class Quote(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        self.label = ""
        self.text = "\\\""

    def getInitializationCode(self):
        return ""

    def getType(self):
        return "Quote"

    def getText(self):
        return self.text


class TextBox(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        self.label = lines[1]

    def getInitializationCode(self):
        return "self.w" + str(self.guiNumber) + " = ATextField()\n        self.w" + str(self.guiNumber) + ".setMaximumHeight(27)"

    def getType(self):
        return "TextBox"

class Option(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        self.label = lines[1]
        self.text = lines[2]

    def getInitializationCode(self):
        return "self.w" + str(self.guiNumber) + " = QtGui.QCheckBox(\"" + self.getLabel() + "\")\n        self.w" + str(self.guiNumber) + ".setStyleSheet(\"color:#11ff33; border-width: 0.0px; border-style: none\")"

    def getType(self):
        return "Option"

# Choices with the same name are grouped together a radio groups in the GUI dialog
class Choice(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        self.group = lines[1]
        self.label = lines[2]
        self.text = lines[3]
        aGroup = None
        if not groupExists(self.group):
           aGroup = Group(self.group)
           groups.append(aGroup) 
        aGroup = getGroup(self.group)
        aGroup.addWidgetNumber(guiNumber)

    def getInitializationCode(self):
        return "self.w" + str(self.guiNumber) + " = QtGui.QRadioButton(\"" + self.getLabel() + "\")\n        self.w" + str(self.guiNumber) + ".setStyleSheet(\"color:#11ff33; border-width: 0.0px; border-style: none;\")"

    def getType(self):
        return "Choice"
  
    def getGroup(self):
        return self.group

class PasteSelection(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        aGroup = None

    def getInitializationCode(self):
        return ""

    def getType(self):
        return "PasteSelection"
  
    def getGroup(self):
        return self.group

class PasteClipboard(TextProvider):
    def __init__(self, lines, guiNumber):
        TextProvider.__init__(self, guiNumber)
        aGroup = None

    def getInitializationCode(self):
        return ""

    def getType(self):
        return "PasteClipboard"
  
    def getGroup(self):
        return self.group

class Group:
    def __init__(self, name):
        self.name = name
        self.widgetNumbers = []
    def addWidgetNumber(self, number):
        self.widgetNumbers.append(number)
    def includesWidgetNumber(self, number):
        for n in self.widgetNumbers:
            if number == n:
                return True
        return False

    def getName(self):
        return self.name

    def getWidgetNumbers(self):
        return self.widgetNumbers

textProviders = []

groups = []


def groupExists(name):
    for group in groups:
        if group.getName() == name:
            return True
    return False

def getGroup(name):
    for group in groups:
        if group.getName() == name:
            return group
    return None

def addEscapeCharacters(text):
    filtered = ""
    for char in text:
        if char == "\"" or char == "\'":
            filtered = filtered + "\\"
        filtered = filtered + char
    return filtered

def main():
    global title
   
    number = 1
    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip("\n")
        lines = []
        lines.append(line)
        if line.startswith("literal"):
            lines.append(sys.stdin.readline().strip("\n"))
            textProviders.append(Literal(lines, number))
            number = number + 1
        elif line.startswith("option"):
            lines.append(sys.stdin.readline().strip())
            lines.append(sys.stdin.readline().strip("\n"))
            textProviders.append(Option(lines, number))
            number = number + 1
        elif line.startswith("choice"):
            lines.append(sys.stdin.readline().strip())
            lines.append(sys.stdin.readline().strip())
            lines.append(sys.stdin.readline().strip("\n"))
            textProviders.append(Choice(lines, number))
            number = number + 1
        elif line.startswith("textbox"):
            lines.append(sys.stdin.readline().strip())
            textProviders.append(TextBox(lines, number))
            number = number + 1
        elif line.startswith("title"):
            title = sys.stdin.readline().strip()
        elif line.startswith("pasteselect"):
            textProviders.append(PasteSelection(lines, number))
            number = number + 1
        elif line.startswith("pasteclip"):
            textProviders.append(PasteClipboard(lines, number))
            number = number + 1
        elif line.startswith("space"):
            textProviders.append(Space(lines, number))
            number = number + 1
        elif line.startswith("quote"):
            textProviders.append(Quote(lines, number))
            number = number + 1

    print "import sys"
    print "import os"
    print "import subprocess"
    print "import re"
    print "import cgi"
    print "import time"
    print "from PyQt4 import QtCore"
    print "from PyQt4 import QtGui"
    print "#import widget_a_group_box"
    print "#import widget_a_text_field"
    print "#import widget_a_label"


    print "class AGroupBox(QtGui.QGroupBox):"
    print "    def __init__(self, parent):"
    print "        QtGui.QGroupBox.__init__(self, parent)"
    print "        self.setStyleSheet(\"color:#ffaa11; border-width: 15.0px; border-style: hidden;\")"
    print ""
    print "    def mousePressEvent(self, event):"
    print "        self.parentWidget().mousePressEvent(event)"
    print ""
    print "    def keyPressEvent(self, event):"
    print "        QtGui.QGroupBox.keyPressEvent(self, event)"
    print "        self.parentWidget().keyPressEvent(event)"
    print ""
    print ""
    print "class ALabel(QtGui.QLabel):"
    print "    def __init__(self):"
    print "        QtGui.QLabel.__init__(self, '')"
    print ""
    print "    def mousePressEvent(self, event):"
    print "        self.parentWidget().mousePressEvent(event)"
    print ""
    print "    def keyPressEvent(self, event):"
    print "        QtGui.QTextEdit.keyPressEvent(self, event)"
    print "        self.parentWidget().keyPressEvent(event)"
    print ""
    print "class ATextField(QtGui.QTextEdit):"
    print "    def __init__(self, label):"
    print "        QtGui.QTextEdit.__init__(self, '')"
    print "        self.label = label"
    print "        self.setStyleSheet(\"background-color : white; border-width: 0.0px; border-style: none;\");"
    print ""
    print "    def __init__(self):"
    print "        QtGui.QTextEdit.__init__(self, '')"
    print "        self.label = 'default'"
    print "        self.setStyleSheet(\"background-color : white; border-width: 0.0px; border-style: none;\");"
    print ""
    print "    def mousePressEvent(self, event):"
    print "        self.parentWidget().mousePressEvent(event)"
    print ""
    print "    def keyPressEvent(self, event):"
    print "        QtGui.QTextEdit.keyPressEvent(self, event)"
    print "        self.parentWidget().keyPressEvent(event)"
    print ""
    print "    def getLabel():"
    print "        return self.label"
    print ""
    print "    def getLabel():"
    print "        return self.label"
    print ""
    print ""
    print "class AFrame(QtGui.QFrame):"
    print "    def getTitle(self):"
    print "        return \"" + title + "\""
    print "    def __init__(self):"
    print "        QtGui.QFrame.__init__(self)"
    print "        self.maximumWidth = 150"

    print "        vLayout = QtGui.QVBoxLayout(self)"

    number = 1
    for text in textProviders:
        if text.getType() == "TextBox":
            print "        label = QtGui.QLabel()"
            print "        label.setStyleSheet(\"color:#ffaa11; border-width: 0px; border-style: none;\")"
            print "        label.setMaximumHeight(30)"
            print "        label.setText(\"" + text.getLabel() + "\")"
            print "        vLayout.addWidget(label, 1)"
        print "        " + text.getInitializationCode()
        if not text.getType() == "Choice" and not text.getType() == "Literal" and not text.getType() == "PasteSelection" and not text.getType() == "PasteClipboard" and not text.getType() == "Space" and not text.getType() == "Quote":
            print "        " + "vLayout.addWidget(self.w" + str(number) + ", 1)"
        number = number + 1

    groupNumber = 1
    for group in groups:
        varName = "group" + str(groupNumber)
        print "        " + varName + " = AGroupBox(self)"
        print "        " + varName + ".setTitle(\"" + group.getName() + "\")"
        print "        " + varName + "Layout = QtGui.QVBoxLayout()"
        firstInGroup = True
        for n in group.getWidgetNumbers():
            print "        " + varName + "Layout.addWidget(self.w" + str(n) + ")"
            if firstInGroup:
                print "        self.w" + str(n) + ".setChecked(True)"
                firstInGroup = False

        print "        " + varName + ".setLayout(" + varName + "Layout)"
        print "        vLayout.addWidget(" + varName + ", 1)"
        groupNumber = groupNumber + 1

    print

    for n in range(1, len(textProviders) + 1):
        currType = textProviders[n - 1].getType()
        if not currType == "Literal" and not currType == "PasteSelection" and not currType == "PasteClipboard" and not currType == "Space" and not currType == "Quote":
            print "        self.connect(self.w" + str(n) + ", QtCore.SIGNAL('clicked()'), self.goPressed)"
 
    #print "        self.setFrameStyle(QtGui.QFrame.Sunken)"
    print "        self.setLineWidth(0)"
    print "        self.setFrameShape(QtGui.QFrame.Box)"

    print "        global the_widget"
    print "        the_widget = self"

    print "    def mousePressEvent(self, event):"
    print "        self.mainAction()"
    print "    def keyPressEvent(self, event):"
    print "        self.mainAction()"
    print "    def goPressed(event):"
    print "        global the_widget"
    print "        the_widget.mainAction()"
    print "    def mainAction(widget):"
    print "        global the_widget"
    print "        text = \"\"" 

    for n in range(1, len(textProviders) + 1):
        if textProviders[n - 1].getType() == "Literal" or textProviders[n - 1].getType() == "Space" or textProviders[n - 1].getType() == "Quote":
            print "        text = text + \"" + textProviders[n - 1].getText() + "\""
        elif textProviders[n - 1].getType() == "Option" or textProviders[n -1].getType() == "Choice":
            print "        if the_widget.w" + str(n) + ".isChecked():"
            print "            text = text + \"" + textProviders[n - 1].getText() + "\"" 
            print "            text = text + \" \""
        elif textProviders[n - 1].getType() == "TextBox":
            print "        text = text + the_widget.w" + str(textProviders[n - 1].getGuiNumber()) + ".toPlainText()"
        elif textProviders[n - 1].getType() == "PasteSelection":
            print "        text = text + QtGui.QApplication.clipboard().text(1)"
        elif textProviders[n - 1].getType() == "PasteClipboard":
            print "        text = text + QtGui.QApplication.clipboard().text(0)"

    print "        # Paste to the clipboard"
    print "        #QtGui.QApplication.clipboard().clear(0)"
    print "        #QtGui.QApplication.clipboard().setText(text, 0)"
    print "        # Paste to the selection"
    print "        QtGui.QApplication.clipboard().clear(1)"
    print "        QtGui.QApplication.clipboard().setText(text, 1)"
    
    print "the_widget = 0"

    print "class CommandMeDialog(QtGui.QDialog):"
    print "    def __init__(self):"
    print "        QtGui.QDialog.__init__(self)"
    print "        commandBox1 = AFrame()"
    print "        self.setWindowTitle(commandBox1.getTitle())"
    print "        hLayoutAll = QtGui.QHBoxLayout(self)"
    print "        self.setMaximumWidth(150)"
    print "        self.setMaximumHeight(1)"
    print "        hLayoutAll.addWidget(commandBox1, 1)"
    print "        self.setStyleSheet(\"background-color : #444444; border-color: #444444; border-width: 1.5px; border-style: groove;\");"
    print ""
    print ""
    print "app = QtGui.QApplication([])"
    print "dialog = CommandMeDialog()"
    print "result = dialog.exec_()"

   
if __name__ == '__main__': main()
