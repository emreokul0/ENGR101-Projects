#Emre Okul and Reyhan Yuruk are group member
#Reference list at the bottom

#it calls tk library in order to create Tkinter module
from Tkinter import *
from recommendations import *
import tkFileDialog
root = Tk() #we created Tk root which is a window.

class Window(Frame):
    """"
    This class builds the graphical user interface of the tool.  This has an object of the data center class as one of
    its attributes. For any data needs and file parsing, GUI uses this object as the gateway
    """

    def __init__(self,parent):

        Frame.__init__(self,parent)
        self.data_center=Data_Center()
        self.initUI()

    def initUI(self):

        self.caption = Label(self, text='Protein Function Prediction Tool', bg='palegreen2',
                             fg='white', font=('', '21', 'bold'), height=2)
        self.caption.pack(fill=X)

        self.frame_1 = Frame(self)
        self.frame_1.pack()

        self.upload_button_1 = Button(self.frame_1, text='Upload\nAnnotations', command=self.data_center.gaf_save,
                                      font=('', '10', 'bold'),
                                      height=2, width=10)
        self.upload_button_1.pack(side=LEFT, pady=30, padx=25)

        self.upload_button_2 = Button(self.frame_1, text='Upload Evidence\nCode Values',
                                      command=self.data_center.txt_save,
                                      font=('', '10', 'bold'),
                                      height=2, width=14)
        self.upload_button_2.pack(side=LEFT, pady=30,padx=25)

        self.upload_button_3 = Button(self.frame_1, text='Upload GO File',
                                      command=self.data_center.obo_save,
                                      font=('', '10', 'bold'),
                                      height=1, width=12)
        self.upload_button_3.pack(side=LEFT, pady=30, padx=25)

        self.frame_2 = Frame(self)
        self.frame_2.pack(side=LEFT, padx=(30,0))

        self.header_1 = Label(self.frame_2, text='Proteins', font=('', '10', 'bold'))
        self.header_1.pack()

        self.scrollbar_1 = Scrollbar(self.frame_2)
        self.listbox_1 = Listbox(self.frame_2, selectmode='single', yscrollcommand=self.scrollbar_1.set,
                                 height=13, width=30)
        self.scrollbar_1.config(command=self.listbox_1.yview)
        self.listbox_1.pack(side=LEFT)
        self.scrollbar_1.pack(side=LEFT, fill=Y)
        self.listbox_1.bind("<<ListboxSelect>>", self.onClick)
        """
        Once the annotation data is uploaded, protein names for each protein from the annotation data file are 
        displayed. This Listbox displays protein names.
        """


        self.frame_3 = Frame(self)
        self.frame_3.pack(side=LEFT)

        self.header_2 = Label(self.frame_3, text='Similarity Metric', font=('', '10', 'bold'))
        self.header_2.pack()

        self.label_free_1 = Label(self.frame_3, borderwidth=2, relief="solid")
        self.var = StringVar()
        self.var.set('Euclidean') ##Euclidean is selected by default
        self.checkbutton_1 = Checkbutton(self.label_free_1, text='Pearson', variable=self.var, onvalue='Pearson',
                                         command=self.onClick_forcheckbutton)
        self.checkbutton_1.pack(padx=20, pady=(20, 0))
        self.checkbutton_2 = Checkbutton(self.label_free_1, text='Euclidean', variable=self.var, onvalue='Euclidean',
                                         command=self.onClick_forcheckbutton)
        self.checkbutton_2.pack(pady=(0, 135))
        self.label_free_1.pack(side=LEFT, padx=40)

        self.frame_4 = Frame(self)
        self.frame_4.pack(side=LEFT)

        self.header_3 = Label(self.frame_4, text='Similar Protein', font=('', '10', 'bold'))
        self.header_3.pack()

        self.scrollbar_2 = Scrollbar(self.frame_4)
        self.listbox_2 = Listbox(self.frame_4, selectmode='single', yscrollcommand=self.scrollbar_2.set,
                                 height=13, width=45)
        self.listbox_2.pack(side=LEFT)
        self.scrollbar_2.pack(side=LEFT, fill=Y)

        self.frame_5 = Frame(self)
        self.frame_5.pack(side=LEFT, padx=20)

        self.header_4 = Label(self.frame_5, text='Predicted Function', font=('', '10', 'bold'))
        self.header_4.pack()

        self.scrollbar_3 = Scrollbar(self.frame_5)
        self.listbox_3 = Listbox(self.frame_5, selectmode='single', yscrollcommand=self.scrollbar_3.set,
                                 height=13, width=70)
        self.listbox_3.pack(side=LEFT)
        self.scrollbar_3.pack(side=LEFT, fill=Y)

        #All listboxes contains scrollbars that allow scrolling along the y-axis.


        self.pack(fill=X)

    def onClick(self,event):
        """
        Once all the files have been uploaded, the user selects a protein from the listbox containing protein names and
         selects a similarity metric in terms of checkbuttons

        """

        self.listbox_2.delete(0,END)
        self.listbox_3.delete(0,END)

        self.protein_names = {}
        self.items = {}
        self.finding_id = {}

        for id in self.data_center.proteins:
            self.protein_names.setdefault(self.data_center.proteins[id].protein_name,{})
            for go_id in self.data_center.proteins[id].annotation_data:
                try:
                    self.protein_names[self.data_center.proteins[id].protein_name][
                        self.data_center.proteins[id].annotation_data[go_id].func.go_id] = (
                        int(self.data_center.proteins[id].annotation_data[go_id].evc.numerical_value))
                except:
                    self.protein_names[self.data_center.proteins[id].protein_name][
                        self.data_center.proteins[id].annotation_data[go_id].func.go_id] = (
                        float(self.data_center.proteins[id].annotation_data[go_id].evc.numerical_value))

        for id in self.data_center.proteins:
            if self.data_center.proteins[id] not in self.finding_id:
                self.finding_id[self.data_center.proteins[id].protein_name] = id

        if app.var.get() == "Euclidean":
            """
            After selecting a protein and a similarity metric, proteins that are similar to the currently selected 
            protein are automatically listed in the listbox in the middle
            """

            protein = self.listbox_1.get(self.listbox_1.curselection()[0])

            scores = topMatches(self.protein_names, protein, n=len(self.protein_names), similarity=sim_distance)

            for index in range(len(scores)):
                if scores[index][0] <= 0:
                    continue
                app.listbox_2.insert(END, str(round(scores[index][0],1)) + " - " + self.finding_id[scores[index][1]] + " - " +
                                     scores[index][1])

            points = getRecommendations(self.protein_names, protein, similarity=sim_distance)

            for index in range(len(points)):
                if points[index][0] <= 0:
                    continue
                app.listbox_3.insert(END, str(round(points[index][0],1)) + " - " + points[index][1] + " - " +
                                     self.data_center.obo_dict[points[index][1]])

        elif app.var.get() == "Pearson":
            """
            Predicted functions for the selected protein are also automatically be displayed in the listbox at the 
            rightmost part
            """

            protein = self.listbox_1.get(self.listbox_1.curselection()[0])

            scores = topMatches(self.protein_names, protein, n=len(self.protein_names), similarity=sim_pearson)

            for index in range(len(scores)):
                if scores[index][0] <= 0:
                    continue
                app.listbox_2.insert(END, str(round(scores[index][0],1)) + " - " + self.finding_id[scores[index][1]] + " - " +
                                     scores[index][1])

            points = getRecommendations(self.protein_names, protein, similarity=sim_pearson)

            for index in range(len(points)):
                if points[index][0] <= 0:
                    continue
                app.listbox_3.insert(END, str(round(points[index][0],1)) + " - " + points[index][1] + " - " +
                                     self.data_center.obo_dict[points[index][1]])

    def onClick_forcheckbutton(self):
        """
        Once all the files have been uploaded, the user selects a protein from the listbox containing protein names and
         selects a similarity metric via checkbuttons on the right

        """

        self.listbox_2.delete(0, END) #these are freshes the listboxes for each protein, otherwise function would added
        self.listbox_3.delete(0, END) #traits of next protein under the before one

        self.protein_names = {}
        self.items = {}
        self.finding_id = {}

        for id in self.data_center.proteins:
            self.protein_names.setdefault(self.data_center.proteins[id].protein_name, {})
            for go_id in self.data_center.proteins[id].annotation_data:
                try:
                    self.protein_names[self.data_center.proteins[id].protein_name][
                        self.data_center.proteins[id].annotation_data[go_id].func.go_id] = (
                        int(self.data_center.proteins[id].annotation_data[go_id].evc.numerical_value))
                except:
                    self.protein_names[self.data_center.proteins[id].protein_name][
                        self.data_center.proteins[id].annotation_data[go_id].func.go_id] = (
                        float(self.data_center.proteins[id].annotation_data[go_id].evc.numerical_value))

        for id in self.data_center.proteins:
            if self.data_center.proteins[id] not in self.finding_id:
                self.finding_id[self.data_center.proteins[id].protein_name] = id

        if app.var.get() == "Euclidean":
            """
            After selecting a protein and a similarity metric, proteins that are similar to the currently selected 
            protein are automatically listed in the listbox in the middle
            """

            protein = self.listbox_1.get(self.listbox_1.curselection()[0])

            scores = topMatches(self.protein_names, protein, n=len(self.protein_names), similarity=sim_distance)

            for index in range(len(scores)):
                if scores[index][0] <= 0:
                    continue
                app.listbox_2.insert(END, str(round(scores[index][0],1)) + " - " + self.finding_id[scores[index][1]] + " - " +
                                     scores[index][1])

            points = getRecommendations(self.protein_names, protein, similarity=sim_distance)

            for index in range(len(points)):
                if points[index][0] <= 0:
                    continue
                app.listbox_3.insert(END, str(round(points[index][0],1)) + " - " + points[index][1] + " - " +
                                     self.data_center.obo_dict[points[index][1]])

        elif app.var.get() == "Pearson":
            """
            Predicted functions for the selected protein are also automatically be displayed in the listbox at the 
            rightmost part
            """

            protein = self.listbox_1.get(self.listbox_1.curselection()[0])

            scores = topMatches(self.protein_names, protein, n=len(self.protein_names), similarity=sim_pearson)

            for index in range(len(scores)):
                if scores[index][0] <= 0:
                    continue
                app.listbox_2.insert(END, str(round(scores[index][0],1)) + " - " + self.finding_id[scores[index][1]] + " - " +
                                     scores[index][1])

            points = getRecommendations(self.protein_names, protein, similarity=sim_pearson)

            for index in range(len(points)):
                if points[index][0] <= 0:
                    continue
                app.listbox_3.insert(END, str(round(points[index][0],1)) + " - " + points[index][1] + " - " +
                                     self.data_center.obo_dict[points[index][1]])

class Functionality(): #This is the class that represents a functionality, it has each GO terms id and name as its attributes

    def __init__(self,id):
        self.go_id=id
        self.go_name=0

class Evc():
    # This is the class that represents an evidence code with attributes evidence code acronym and its numeric value.

    def __init__(self,evidence_code):
        self.evidence_code=evidence_code
        self.numerical_value=0

class Function():
    """This is the class that represents an annotation of a protein by a functionality. It has two attributes:
    functionality (type: a GO object) and evidence code (type: an Evidence Code object)."""

    def __init__(self,func_id,evc):
        self.func=Functionality(func_id)
        self.evc=Evc(evc)

class Protein():
    """
    This is the class that represents a protein. It has each proteins id, name, and
    annotations as its attributes. (type: a dictionary of annotation objects - key: GO id from the
    annotation objects GO term, value: Annotation object)
    """


    def __init__(self,id,name):
        self.protein_id=id
        self.protein_name=name
        self.annotation_data={}

class Data_Center():
    """
    This class represents application,s data center. There are three methods inside it; one method that reads and parses
    the data included in the GO file (go.obo); one method that reads and parses the data included in the annotation
    file (GEO_human.gaf); one method that reads and parses the data included in the ecv.txt file.
    """

    def __init__(self):
        self.proteins={}
        self.evcs={}

    def gaf_save(self):

        """
        When the user clicks on the -Upload Annotations- button, this method works. By clicking this button, the user
        uploads the Annotation Data. In the annotation file (GEO_human.gaf), each line specifies an
        annotation of a protein with a functionality. Each protein may have multiple annotations each of which is stored
        on a separate line. Method extracts protein id, protein name, functionality annotation and evidence code which
        are located in columns 2, 3, 4, and 6.
        """

        self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("Plain Text", "*.gaf"), ("all files", "*.*")))

        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith('!'): ###it skips the first 15 lines which are beginnigg with -!-
                    continue
                if line.split('\t')[1] in self.proteins:
                    self.proteins[line.split('\t')[1]].annotation_data[line.split('\t')[4]]=\
                        Function(line.split('\t')[4],line.split('\t')[6])
                else:
                    self.proteins[line.split('\t')[1]] = Protein(line.split('\t')[1],line.split('\t')[2])
                    self.proteins[line.split('\t')[1]].annotation_data[line.split('\t')[4]]=\
                        Function(line.split('\t')[4],line.split('\t')[6])
        file.close()

        for id in self.proteins:
            name = self.proteins[id].protein_name
            app.listbox_1.insert(END,name)

    def txt_save(self):

        """
        When the user clicks on the -Upload Evidence Code Values- button, this method works. In the
        evidence code values file (ecv.txt), for each evidence code that we extracted in the above method, there is a
        corresponding numerical value in a tab-separated manner. It is using these values as a kind of rating for
        the annotation.

        """

        self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("Plain Text", "*.txt"), ("all files", "*.*")))

        with open(self.filename, 'r') as file:
            for line in file:
                self.evcs[line.split('\t')[0]] = line.split('\t')[1].strip('\n')
        file.close()

        for id in self.proteins:
            for go_id in self.proteins[id].annotation_data:
                evc = float(self.evcs[self.proteins[id].annotation_data[go_id].evc.evidence_code])
                self.proteins[id].annotation_data[go_id].evc.numerical_value = evc

    def obo_save(self):

        """
        When the user clicks on the -Upload GO File- button, this method works. In the GO data file (go.obo), names
        corresponding to each GO id stored. In the file, the id of a GO term is provided, then on the next line, its name is
        included. Method uses GO term names to display the predicted functionalities.

        """

        self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("Plain Text", "*.obo"), ("all files", "*.*")))

        self.obo_dict = {}

        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith('id:'):
                    id = line.strip('id: \n')
                if line.startswith('name:'):
                    self.obo_dict[id] = line.strip('name: \n')
        file.close()

        for id in self.proteins:
            for go_id in self.proteins[id].annotation_data:
                name = self.obo_dict[self.proteins[id].annotation_data[go_id].func.go_id]
                self.proteins[id].annotation_data[go_id].func.go_name = name

root.title('Protein Function Prediction Tool') #name of the window
root.geometry('1200x500+100+100') #sizes of the window
app = Window(root)
root.mainloop()

# References
# https://www.tutorialspoint.com/python/tk_scrollbar.htm
# https://pythonspot.com/tk-file-dialogs/
# https://www.tutorialspoint.com/python/string_startswith.htm
# http://effbot.org/tkinterbook/scrollbar.htm
# https://www.programiz.com/python-programming/methods/string/strip
# https://www.tutorialspoint.com/python/tk_listbox.htm
# https://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
# https://stackoverflow.com/questions/49496930/python-tkinter-delete-all-contents-from-listbox

