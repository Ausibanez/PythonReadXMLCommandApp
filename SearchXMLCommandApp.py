import SearchXMLCommand
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

def main():
    SearchXML = SearchXMLCommand()
    xml_file_name = SearchXMLCommand.choose_xml_file()

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

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        sys.exit()

root = Tk()
root.geometry('900x200')
root.title("Search XMLCommand")
app = main()
root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
root.destroy()
