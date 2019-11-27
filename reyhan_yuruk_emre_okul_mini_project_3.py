#Reference list at the bottom

# firstly we called libraries in order to use them
from Tkinter import *
from ttk import Combobox
from PIL import ImageTk
from clusters import *
import tkFileDialog
root = Tk() #we created Tk root which is a window.

class Window(Frame):
    """
    This class builds the graphical user interface of the tool. It has an object of the data center class as one of
    its attributes.
    """

    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.controller = 0
        self.var = 'empty'
        self.data_center = DataCenter()
        self.initUI()

    def initUI(self):

        self.caption = Label(self, text='Election Data Analysis Tool v. 1.0', bg='red',
                             fg='white', font=('', '21', 'bold'), height=1)
        self.caption.pack(fill=X)

        self.load_button = Button(self, text='Load Election Data', relief=RIDGE, font=('', '10'),
                                  bg='gray85', height=2, width=35, command=self.data_center.save_results)
        self.load_button.pack(pady=(8, 12))

        self.frame_1 = Frame(self)
        self.frame_1.pack()

        self.cluster_districts_button = Button(self.frame_1, text='Cluster Districts', relief=RIDGE, height=3, width=35,
                                               command=self.cluster_districts, font=('', '10'), bg='gray85')
        self.cluster_districts_button.pack(side=LEFT, padx=(0, 2))

        self.cluster_parties_button = Button(self.frame_1, text='Cluster Political Parties', relief=RIDGE, bg='gray85',
                                             command=self.cluster_parties, font=('', '10'), height=3, width=35)
        self.cluster_parties_button.pack(side=LEFT)

        self.pack(fill=X)

    def initUI_extra(self):

        self.frame_2 = Frame(self)
        self.frame_2.pack()

        self.canvas = Canvas(self.frame_2, bg="gray", height=320, width=1100, scrollregion=(0, 0, 1280, 1650))
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        self.scrollbar_y = Scrollbar(self.frame_2, orient=VERTICAL)
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=0, sticky=N + S + E)
        #horizontal and vertical scroll bars for displaying image in the canvas
        self.scrollbar_x = Scrollbar(self.frame_2, orient=HORIZONTAL)
        self.scrollbar_x.config(command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky=S + E + W)

        self.canvas.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.frame_3 = Frame(self)
        self.frame_3.pack()

        self.label_1 = Label(self.frame_3, text='Districts:')
        self.label_1.pack(side=LEFT)

        self.listbox = Listbox(self.frame_3, selectmode='multiple', height=10, width=25)
        self.listbox.pack(side=LEFT)

        self.scrollbar_for_listbox = Scrollbar(self.frame_3, orient=VERTICAL)
        self.scrollbar_for_listbox.config(command=self.listbox.yview)
        self.scrollbar_for_listbox.pack(side=LEFT, fill=Y)
        """
        The listbox includes the names of the districts from the uploaded file in a sorted way. It allows for 
        multiple selections
        """
        self.listbox.config(yscrollcommand=self.scrollbar_for_listbox.set)
        for district in sorted(self.data_center.district):
            self.listbox.insert(END, district)

        self.label_2 = Label(self.frame_3, text='Threshold:')
        self.label_2.pack(side=LEFT)
        """
        If the selected value in combobox is less, thresold eliminates from the analysis, the matrix entry for the 
        eliminated party is 0 for that district.
        """
        self.combobox = Combobox(self.frame_3, state="readonly", values=['0%', '1%', '10%', '20%', '30%', '40%', '50%'], width=5)
        self.combobox.pack(side=LEFT)
        self.combobox.set('0%') #0 is default selection

        self.analysis_button = Button(self.frame_3, text='Refine Analysis', command=self.data_analysis, relief=RIDGE,
                                      bg='gray85', height=2, width=35)
        self.analysis_button.pack(side=LEFT)

    def cluster_districts(self):
        """
        When the user click to the -Cluster Districts- button, the above clustering task will be initiated by using
        the hierarchical clustering, and the resulting dendrogram will be displayed below the button row, the labels in
        this dendrogram are the district names.
        """

        if self.controller == 0:
            self.initUI_extra()
            self.controller = 1

        self.var = 'districts'
        self.data_analysis()

    def cluster_parties(self):
        """
        When the users click to the -Cluster Political Parties- button, the above clustering task will be initiated
        by using the hierarchical clustering, and the resulting dendrogram will be displayed below the button row.
        The labels in the dendrogram are the abbreviations of the political party names.
        """

        if self.controller == 0:
            self.initUI_extra()
            self.controller = 1

        self.var = 'parties'
        self.data_analysis()

    def data_analysis(self):
        """
        When the user clicks on the -Refine Analysis- button, the current clustering will be re-run according to
        the selections in the listbox and combobox.
        """

        self.percentage = float(self.combobox.get().strip('%'))
        self.used_dict = {}

        if len(self.listbox.curselection()) != 0:
            #when the user chooses a set  of districts from the listbox, the analysis are performes only with the selected districts
            self.districts_list = [sorted(self.data_center.district)[index] for index in self.listbox.curselection()]

        else:
            #If no district is chosen from the listbox, then all the districts  are  includes in the analysis as default
            self.districts_list = sorted(self.data_center.district)

        for district in self.districts_list:
            self.used_dict.setdefault(district, {})
            for party in self.data_center.party:
                vote = self.data_center.districts[district].election_results[party]
                if float(vote) < self.percentage:
                    self.used_dict[district][party] = '0'
                else:
                    self.used_dict[district][party] = vote

        with open('Election_Details.txt', 'w') as file:
            file.write('Election\t')
            for party in self.data_center.party:
                file.write(party + '\t')
            for district in self.districts_list:
                file.write('\n')
                file.write(district)
                for party in self.data_center.party:
                    file.write('\t' + self.used_dict[district][party])

        rownames, colnames, data = readfile('Election_Details.txt')

        if self.var == 'parties':
            data = rotatematrix(data)
            rownames, colnames = colnames, rownames

        clust = hcluster(data, distance=sim_distance)
        drawdendrogram(clust, rownames)
        self.image = ImageTk.PhotoImage(Image.open('clusters.jpg'))
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        self.data_center.save_results()

class District(): #This is the class that represents a district with attributes name

    def __init__(self, district_name):
        self.district_name = district_name
        self.election_results = {}

class PoliticalParty(): #This is the class that represents a political party with attributes acronym

    def __init__(self, political_party_name):
        self.political_party_name = political_party_name
        self.election_results = {}

class DataCenter():
    """
    This is the class that represents the application,s data center. It has a method that reads and parses the data
    included in the election results file, and populates its attributes.
    """

    def __init__(self):

        self.districts = {}
        self.parties = {}
        self.control_point = 0

    def save_results(self):
        """
        This method parses the district name, the abbreviation of each political party, and percentage of votes for
        each political party in each district
        """

        if self.control_point == 0:

            self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("Plain Text", "*.txt"), ("all files", "*.*")))

            #Once the file is loaded, the program parses the file and prepare them to be used for in the clustering process

            self.control_point = 1

        with open(self.filename, 'r') as file:
            self.results = {}
            self.party = []
            self.district = []
            district = ''
            for line in file:
                if line.startswith('Kaynak: YSK'): #district name always comes after a line that contains 'Kaynak: YSK'
                    district += next(file).strip('\n')
                if line.startswith('Kis.'):
                    while True:
                        line = next(file)
                        if line.startswith('Toplam'):
                            break
                        if line.startswith('BGMSZ'): #ignoring results for BGMSZ
                            continue
                        item = line.split('\t')
                        if district == '':
                            district = 'Adalar'
                        self.results.setdefault(district, {})
                        self.results[district][item[0]] = item[4].strip('%\n')
                        if item[0] not in self.party:
                            self.party.append(item[0])
                        if district not in self.district:
                            self.district.append(district)
                    district = ''

        for district in self.results:
            for party in self.party:
                self.districts.setdefault(district, District(district))
                self.districts[district].district_name = district
                if party not in self.results[district]:
                #If there is no data for a political party in a given district, then the corresponding party vote will be the 0
                    self.districts[district].election_results[party] = '0'
                else:
                    self.districts[district].election_results[party] = self.results[district][party]

        for party in self.party:
            for district in self.results:
                self.parties.setdefault(party, PoliticalParty(party))
                self.parties[party].district_name = party
                if party not in self.results[district]:
                    self.parties[party].election_results[district] = '0'
                else:
                    self.parties[party].election_results[district] = self.results[district][party]

root.title('Clustering') #name of the window
root.geometry('1200x700') #sizes of the window
app = Window(root)
root.mainloop()

#References
# https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python
# https://stackoverflow.com/questions/7727804/tkinter-using-scrollbarson-a-canvas
# https://www.tutorialspoint.com/python/tk_scrollbar.htm
# https://pythonspot.com/tk-file-dialogs/
# https://stackoverflow.com/questions/47500266/python-tkinter-combobox
# https://stackoverflow.com/questions/19646752/python-scrollbar-on-text-widget
# https://stackoverflow.com/questions/32399158/read-next-line-after-a-matching-line-in-python