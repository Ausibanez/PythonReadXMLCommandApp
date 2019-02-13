## Reads one line at a time from a file containing multiple lines of
## full xml tags and prints the given attribute's value to a file.
## Useful for reading values from DPP XMLCommand. Can optionally format the
## output to the file.
##
## Example XMLCommand (one line):
##
##<commandrequest><primary>828411-01</primary>##<secondary>Run<value>1</value></secondary>
##<index>16</index><starttime>2018-08-16 14:00:00</starttime>##<runtime>59.98333358764648</runtime>
##<timestamp>1534446000</timestamp>##<offset>-300</offset></commandrequest>
import xml.etree.ElementTree as ET
from tkinter import filedialog
from tkinter import *
from tkinter import scrolledtext
import os

class SearchXMLCommand():

    def __init__(self, parent):
        # Frame setup start
        frameTop = Frame(parent)
        frameTop.grid(row=0, column=0, sticky=E+W)
        frameBottom = Frame(parent)
        frameBottom.grid(row=1, column=0, padx=10, pady=10, sticky=W+E+N+S)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        frameBottom.rowconfigure(0, weight=1)
        frameBottom.columnconfigure(0, weight=1)
        # Frame setup end
        # Create frame contents
        scrolltxt = self.createScrolledText(frameBottom)
        xml_tag = self.createXMLTagEntry(frameTop)
        txtOutput = self.createFormattedOutputEntry(frameTop)
        self.creatOpenButton(scrolltxt, xml_tag, txtOutput, frameTop)
        self.createClearButton(scrolltxt, frameTop)

    # Opens dialog box for user to select an XML file containing a series of XMLCommand values
    def choose_xml_file(self):
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        root = Tk()
        root.withdraw()
        return filedialog.askopenfilename(initialdir = os.path.dirname(current_dir_path),
                                                 title = "Open XMLCommand file",
                                                 filetypes = (("xml files","*.xml"),("all files","*.*")))

    # Opens dialog box for user to select a file to write the output results to
    def choose_save_file(self):
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        return filedialog.asksaveasfilename(initialdir = os.path.dirname(current_dir_path),
                                                defaultextension = '.txt',
                                                filetypes = (("text files","*.txt"),("all files","*.*")),
                                                title = 'Save results to file')

    def logError(self, scroll, msg):
        scroll.configure(state=NORMAL)
        scroll.insert('end', msg, 'error')
        scroll.tag_config('error', foreground='red')
        scroll.configure(state=DISABLED)

    def logGood(self, scroll, msg):
        scroll.configure(state=NORMAL)
        scroll.insert('end', msg, 'good')
        scroll.tag_config('good', foreground='green')
        scroll.configure(state=DISABLED)

    def logInfo(self, scroll, msg):
        scroll.configure(state=NORMAL)
        scroll.insert('end', msg)
        scroll.configure(state=DISABLED)

    # Read file line by line stripping trailing white space
    # and returning only non-blank lines
    def read_nonblank_lines(self, file):
        for l in file:
            line = l.rstrip()
            if line:
                yield line

    # Determines where the xml value token is located and stores the
    # substrings for the output in a list for later
    # Currently only supports one token
    def parseOutputText(self, scroll_widget, txtOutput):
        strList = []
        try:
            outStr = txtOutput.get()
            if not outStr:
                outStr = '{#}'
            strLen = len(outStr)
            tokenPos = outStr.index('{#}')
            strList.append(outStr[:tokenPos])
            strList.append(outStr[tokenPos+3:strLen])
            return strList
        except Exception as e:
            msg = 'Error in output text: ' + str(e) + '\n'
            self.logError(scroll_widget, msg)
            self.logError(scroll_widget, 'Verify the {#} token is included'
                + ' as this is used to set the location of the attribute value'
                + ' in the output')

    def main(self, scroll_widget, xml_tag, txtOutput):
        xml_file_name = self.choose_xml_file()
        if xml_file_name:
            self.logInfo(scroll_widget, 'XMLCommand file is ' + xml_file_name + '\n')
            xml_tag_val = xml_tag.get()
            if xml_tag_val:
                self.logInfo(scroll_widget, 'Retrieving values for tag: ' + xml_tag_val + '\n')
                try:
                    with open(xml_file_name) as inFile:
                        output_file_name = self.choose_save_file()
                        if output_file_name:
                            strList = self.parseOutputText(scroll_widget, txtOutput)
                            if strList:
                                self.logInfo(scroll_widget, 'Output file is ' + output_file_name + '\n')
                                with open(output_file_name, "w") as outFile:
                                    for line in self.read_nonblank_lines(inFile):
                                        tree = ET.ElementTree(ET.fromstring(line))
                                        values = ""
                                        for tag in tree.findall(xml_tag.get()):
                                            for node in tag.getiterator():
                                                values = values + node.text + ' '
                                        #objectname = tree.find(xml_tag.get())
                                        if values is not None:
                                            outFile.write(strList[0] + values + strList[1] + '\n')
                                    self.logGood(scroll_widget, 'Done\n')
                        else:
                            self.logError(scroll_widget, 'Invalid output file name\n')
                except Exception as e:
                    msg = 'Unable to process xml: ' + str(e) + '\n'
                    self.logError(scroll_widget, msg)
            else:
                self.logError(scroll_widget, 'Invalid XML tag\n')
        else:
            self.logError(scroll_widget, 'Invalid XML file name\n')

    # Setup scrolled text widget for message logging
    def createScrolledText(self, frame):
        textBox = scrolledtext.ScrolledText(frame, width=105, height=15)
        textBox.grid(row=0, column=0, sticky=E+W+N+S)
        textBox.configure(state=DISABLED)
        return textBox

    def creatOpenButton(self, scroll, xml_tag, txtOutput, frame):
        btn_open = Button(frame, text="Open...", command=lambda: self.main(scroll, xml_tag, txtOutput))
        btn_open.grid(row=0, column=0, padx=10, pady=10)

    # Create a tk entry. Input: frame
    def createXMLTagEntry(self, frame):
        tagName = Entry(frame)
        tagName.insert(0,"primary")
        tagName.grid(row=0, column=1)
        return tagName

    def createFormattedOutputEntry(self, frame):
        def setCharLimit(*args):
            value = outputStr.get()
            if len(value) > 200: outputStr.set(value[:200])

        outputStr = StringVar()
        outputStr.trace('w', setCharLimit)
        outText = Entry(frame, textvariable=outputStr)
        outText.config(width=100)
        outText.insert(0,"The xml tag value is {#}")
        outText.grid(row=0, column=2, padx=10, pady=10)
        return outText

    # Delete all text in the scolledText widget
    def clearText(self, scroll):
        scroll.configure(state=NORMAL)
        scroll.delete('1.0', END)
        scroll.configure(state=DISABLED)

    def createClearButton(self, scroll, frame):
        btn_clear = Button(frame, text="Clear log", command=lambda: self.clearText(scroll))
        btn_clear.grid(row=0, column=3, padx=10, pady=10)
