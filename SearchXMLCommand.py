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

    def logError(self, scroll_widget, msg):
        scroll_widget.insert('insert', msg, 'error')
        scroll_widget.tag_config('error', foreground='red')

    def logGood(self, scroll_widget, msg):
        scroll_widget.insert('insert', msg, 'good')
        scroll_widget.tag_config('good', foreground='green')


    # Read file line by line stripping trailing white space
    # and returning only non-blank lines
    def read_nonblank_lines(self, file):
        for l in file:
            line = l.rstrip()
            if line:
                yield line

    def main(self, scroll_widget, xml_tag):
        xml_file_name = self.choose_xml_file()
        scroll_widget.insert('insert', 'Retrieving values for tag: ' + xml_tag.get() + '\n')
        if xml_file_name:
            scroll_widget.insert('insert', 'XMLCommand file is ' + xml_file_name + '\n')
            try:
                with open(xml_file_name) as inFile:
                    output_file_name = self.choose_save_file()

                    if output_file_name:
                        scroll_widget.insert('insert', 'Output file is ' + output_file_name + '\n')
                        with open(output_file_name, "w") as outFile:
                            for line in self.read_nonblank_lines(inFile):
                                tree = ET.ElementTree(ET.fromstring(line))
                                objectname = tree.find(xml_tag.get())
                                # Hard-coded output format. Should make this configurable
                                outFile.write("insert into gasQualityDefine_21aug2018 select '" + objectname.text + "'\n")
                            self.logGood(scroll_widget, 'Done\n')
                    else:
                        scroll_widget.insert('insert', "Invalid output file name\n")
            except Exception as e:
                msg = 'Unable to process xml: ' + str(e) + '\n'
                self.logError(scroll_widget, msg)
        else:
            scroll_widget.insert('insert', "Invalid XML file name\n")

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
        textBox = Text(frame, borderwidth=3, relief="sunken")
        textBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scroll_bar = Scrollbar(frame, command=textBox.yview)
        scroll_bar.grid(row=0, column=1, sticky='nsew')
        #scroll_bar.pack(fill=Y, side=RIGHT)
        textBox['yscrollcommand'] = scroll_bar.set
        return textBox

    # Create a tk entry. Input: frame
    def createTextEntryWidget(self, frame):
        tagName = Entry(frame)
        tagName.insert(0,"primary")
        tagName.pack(side=RIGHT, expand=YES)
        return tagName

    def createButtonWidget(self, scroll, xml_tag, topRow):
        w = Button(topRow, text="Open...", command=lambda: self.main(scroll, xml_tag))
        w.pack(side=LEFT, padx=5, pady=5)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        frameBottom = self.createFrame(BOTTOM, 885, 150)
        text_box = self.createScrollbarTextWidget(frameBottom)
        frameTOP = self.createFrame(TOP, 100, 10)
        xml_tag = self.createTextEntryWidget(frameTOP)
        self.createButtonWidget(text_box, xml_tag, frameTOP)
