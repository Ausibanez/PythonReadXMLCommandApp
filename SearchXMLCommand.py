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
from tkinter import messagebox
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

    def main(self, scroll_widget):
        xml_file_name = self.choose_xml_file()

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
                                # Hard-coded to look at "primary" xml tag
                                # Should re-write to allow user to choose tag (perhaps out of a list of available tags)
                                objectname = tree.find('primary')
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

    # Setup scrolled text widget for message logging
    def createScrollTextWidget(self):
        log = scrolledtext.ScrolledText()
        log.pack(fill=X, expand=True, padx=8, pady=8, side=BOTTOM)
        return log

    def createTextEntryWidget(self):
        row = Frame(self)
        tagName = Entry(row)
        tagName.insert(0,"<tag name>")
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        tagName.pack(side=RIGHT, expand=YES, fill=X)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        scroll_widget = self.createScrollTextWidget()
        self.createTextEntryWidget()
        #self.main(scroll_widget)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        sys.exit()

root = Tk()
root.geometry('900x200')
root.title("Search XMLCommand")
app = SearchXMLCommand(master=root)
root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
root.destroy()
