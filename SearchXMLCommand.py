## Useful for parsing DPP XMLCommand grabbing a specific attribute's value
## and printing it to a line or using it as part of another built string
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

class SearchXMLCommand(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        frameBottom = self.createFrame(BOTTOM, 885, 190)
        scrolltxt = self.createScrollbarTextWidget(frameBottom)
        frameTOP = self.createFrame(TOP, 100, 50)
        xml_tag = self.createXMLTagEntry(frameTOP)
        txtOutput = self.createFormattedOutputEntry(frameTOP)
        self.createButtonWidget(scrolltxt, xml_tag, txtOutput, frameTOP)
        self.createClearButton(scrolltxt, frameTOP)

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
    def parseOutputText(self, scroll_widget, txtOutput):
        strList = []
        try:
            outStr = txtOutput.get()
            if outStr:
                strLen = len(outStr)
                tokenPos = outStr.index('##')
                strList.append(outStr[:tokenPos])
                strList.append(outStr[tokenPos+2:strLen])                
                return strList
        except Exception as e:
            msg = 'Parse output text error: ' + str(e) + '\n'
            self.logError(scroll_widget, msg)

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
                        strList = self.parseOutputText(scroll_widget, txtOutput)
                        if output_file_name:
                            self.logInfo(scroll_widget, 'Output file is ' + output_file_name + '\n')
                            with open(output_file_name, "w") as outFile:
                                for line in self.read_nonblank_lines(inFile):
                                    tree = ET.ElementTree(ET.fromstring(line))
                                    objectname = tree.find(xml_tag.get())
                                    if objectname is not None:
                                        outFile.write(strList[0] + objectname.text + strList[1] + '\n')
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

    # Create a tk frame
    # Inputs: side, width, height
    def createFrame(self, Pos, W, H):
        frame = Frame(self, width=W, height=H)
        frame.pack(fill="both", expand=True, side=Pos)
        frame.grid_propagate(False)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    # Setup scrolled text widget for message logging
    def createScrollbarTextWidget(self, frame):
        textBox = scrolledtext.ScrolledText(frame)
        textBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        textBox.configure(state=DISABLED)
        return textBox

    def createButtonWidget(self, scroll, xml_tag, txtOutput, frame):
        w = Button(frame, text="Open...", command=lambda: self.main(scroll, xml_tag, txtOutput))
        w.grid(row=0, column=0, sticky='w', padx=2, pady=2)

    # Create a tk entry. Input: frame
    def createXMLTagEntry(self, frame):
        frame.grid_columnconfigure(0, weight=0)
        tagName = Entry(frame)
        tagName.insert(0,"primary")
        tagName.grid(row=0, column=1, sticky='w', padx=10, pady=2)
        return tagName

    def createFormattedOutputEntry(self, frame):
        def setCharLimit(*args):
            value = outputStr.get()
            if len(value) > 200: outputStr.set(value[:200])

        outputStr = StringVar()
        outputStr.trace('w', setCharLimit)
        frame.grid_columnconfigure(2, weight=1)
        outText = Entry(frame, textvariable=outputStr)
        outText.config(width=100)
        outText.insert(0,"The xml tag value is ##")
        outText.grid(row=0, column=2, sticky='w', padx=2, pady=2)
        return outText

    # Delete all text in the scolledText widget
    def clearText(self, scroll):
        scroll.configure(state=NORMAL)
        scroll.delete('1.0', END)
        scroll.configure(state=DISABLED)

    def createClearButton(self, scroll, frame):
        frame.grid_columnconfigure(3, weight=1)
        w = Button(frame, text="Clear", command=lambda: self.clearText(scroll))
        w.grid(row=0, column=3, sticky='e', padx=2, pady=2)
