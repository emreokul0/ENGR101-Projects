#emre okul and reyhan yuruk are group member

# firstly we called libraries in order to use them

from Tkinter import *
import ttk, Tkinter, Tkconstants, tkFileDialog, xlrd, xlwt, xlutils
from xlrd import *
from xlwt import *
root = Tk() #we created Tk root which is a window.

class Window(Frame): #in this class, there is the graphical user interface of tool
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.initUI()
        self.student = {}
    def initUI(self):
        self.caption = Label(self, text='Grades Management Tool', bg='mediumspringgreen',
                        fg='white', font=('','25','bold'))
        self.caption.grid(row=0,column=0,columnspan=11,sticky=EW)

        self.select_button = Button(self, text='Select File', command=open_data.read_excel)
        self.select_button.grid(row=1,column=1,columnspan=2,sticky=W,pady=10)
        # select file button is created, details in the read_excel function

        self.tree = ttk.Treeview(self) #treeview widget is created with the ID, Name, Surname columns
        self.tree['columns'] = ('#0', '#1')
        self.tree.column('#0', width=100)
        self.tree.column('#1', width=100)
        self.tree.column('#2', width=100)
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Surname')
        self.tree.grid(row=2,rowspan=6,column=0,columnspan=4,sticky=W,
                       padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", open_data.onClick)

        self.show_button = Button(self, text='Show Data', command=open_data.show_data)
        self.show_button.grid(row=5,column=4,columnspan=2)#adds show button, function plays automatically when the button is clicked.

        self.details = Label(self, text='Student Details:',
                             bg='teal', fg='white', font=('','10','bold'))
        self.details.grid(row=2,column=6,columnspan=6,sticky=EW)

        self.info1 = Label(self, text='Name', font=('','10','bold'))
        self.info1.grid(row=3, column=6, sticky=W, padx=10)

        self.space1 = Label(self, text='          ')
        self.space1.grid(row=3,column=7, sticky=W)

        self.info2 = Label(self, text='Surname', font=('', '10', 'bold'))
        self.info2.grid(row=4, column=6, sticky=W, padx=10)

        self.space2 = Label(self, text='          ')
        self.space2.grid(row=4, column=7, sticky=W)

        self.info3 = Label(self, text='ID', font=('', '10', 'bold'))
        self.info3.grid(row=5, column=6, sticky=W, padx=10)

        self.space3 = Label(self, text='          ')
        self.space3.grid(row=5, column=7, sticky=W)

        self.info4 = Label(self, text='Dept', font=('', '10', 'bold'))
        self.info4.grid(row=6, column=6, sticky=W, padx=10)

        self.space4 = Label(self, text='          ')
        self.space4.grid(row=6, column=7, sticky=W)

        self.info5 = Label(self, text='GPA', font=('', '10', 'bold'))
        self.info5.grid(row=7, column=6, sticky=W, padx=10)

        self.space5 = Label(self, text='          ')
        self.space5.grid(row=7, column=7, sticky=W)

        self.info6 = Label(self, text='MP1 Grade:', font=('', '10', 'bold'))
        self.info6.grid(row=3, column=8, sticky=W, padx=20)

        self.space6 = Label(self, text='                    ')
        self.space6.grid(row=3, column=9, sticky=W)

        self.info7 = Label(self, text='MP2 Grade:', font=('', '10', 'bold'))
        self.info7.grid(row=4, column=8, sticky=W, padx=20)

        self.space7 = Label(self, text='                    ')
        self.space7.grid(row=4, column=9, sticky=W)

        self.info8 = Label(self, text='MP3 Grade:', font=('', '10', 'bold'))
        self.info8.grid(row=5, column=8, sticky=W, padx=20)

        self.space8 = Label(self, text='                    ')
        self.space8.grid(row=5, column=9, sticky=W)

        self.info9 = Label(self, text='MT Grade:', font=('', '10', 'bold'))
        self.info9.grid(row=6, column=8, sticky=W, padx=20)

        self.space9 = Label(self, text='                    ')
        self.space9.grid(row=6, column=9, sticky=W)

        self.info10 = Label(self, text='Final Grade:', font=('', '10', 'bold'))
        self.info10.grid(row=7, column=8, sticky=W, padx=20)

        self.space10 = Label(self, text='                    ')
        self.space10.grid(row=7, column=9, sticky=W)

        self.projects = Label(self, text='Projects:')
        self.projects.grid(row=8, column=0)

        self.mp1 = Label(self, text='MP1')
        self.mp1.grid(row=8, column=1)

        self.mp2 = Label(self, text='MP2')
        self.mp2.grid(row=8, column=2)

        self.mp3 = Label(self, text='MP3')
        self.mp3.grid(row=8, column=3)

        self.mt = Label(self, text='MT')
        self.mt.grid(row=8, column=4)

        self.final = Label(self, text='Final')
        self.final.grid(row=8, column=5)

        self.grades = Label(self, text='Grades:')
        self.grades.grid(row=9, column=0)

        self.export_as = Label(self, text='Export As:')
        self.export_as.grid(row=10, column=0)

        self.entry1 = Entry(self, width=12)
        self.entry1.grid(row=9, column=1)

        self.entry2 = Entry(self, width=12)
        self.entry2.grid(row=9, column=2)

        self.entry3 = Entry(self, width=12)
        self.entry3.grid(row=9, column=3)

        self.entry4 = Entry(self, width=12)
        self.entry4.grid(row=9, column=4)

        self.entry5 = Entry(self, width=12)
        self.entry5.grid(row=9, column=5)

        self.save_button = Button(self, text='Save Grades', command=save.save_grades)
        self.save_button.grid(row=9, column=6)

        self.var = StringVar()
        self.var.set('e')

        self.checkbutton1 = Checkbutton(self, text='csv', variable=self.var, onvalue='csv')
        self.checkbutton1.grid(row=11, column=1)#provides a check box

        self.checkbutton2 = Checkbutton(self, text='txt', variable=self.var, onvalue='txt')
        self.checkbutton2.grid(row=12, column=1)

        self.checkbutton3 = Checkbutton(self, text='xls', variable=self.var, onvalue='xls')
        self.checkbutton3.grid(row=13, column=1)

        self.file_name = Label(self, text='File Name:')
        self.file_name.grid(row=11, column=2, sticky=W)

        self.entry6 = Entry(self, width=20)
        self.entry6.grid(row=11, column=3, columnspan=2, sticky=W)

        self.export_button = Button(self, text='Export Data', command=save.export_data,
                                    height=1, width=33)
        self.export_button.grid(row=12, column=2, columnspan=3, sticky=W)

        self.info = Label(self, text='Program messages...', font=('','7'))
        self.info.grid(row=14, column=0, sticky=W)

        self.grid()

class OpenStudentData():

    def __init__(self):
        self.student={}

    def read_excel(self):
        """"
        When the user presses the 'Select File' button, the program opens a file navigation dialog,
        and asks for a student list in the form of a custom Excel file.
        """
        try:
            self.check_point_1 = True
            self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))

            book = open_workbook(self.filename)

            if self.filename == '' or self.filename.split('/')[-1] != 'Engr Student Data.xlsx':
                self.check_point_1 = False
            if self.check_point_1 == True:
                self.headings = ['ID', 'Name', 'Section', 'Dept', 'GPA', 'MP1 Grade:', 'MP2 Grade:', 'MP3 Grade:',
                                 'MT Grade:', 'Final Grade:']
                book = open_workbook(self.filename)
                sheet = book.sheet_by_index(0)
                for row_index in range(1, sheet.nrows):
                    index = 0
                    traits = []
                    for column_index in range(sheet.ncols):
                        traits.append(sheet.cell(row_index, column_index).value)
                        self.student[sheet.cell(row_index, 1).value] = traits
                        index += 1
                used_list = []
                for key in self.student:
                    used_list.append(key)
                self.sort_list = sorted(used_list)
                for index in range(len(self.sort_list) - 1, -1, -1):
                    single = self.sort_list[index].split(' ')
                    if len(single) == 3:
                        app.tree.insert("", 0, text=int(self.student[self.sort_list[index]][0]),
                                        values=(single[:2], single[2]))
                        continue
                    app.tree.insert("", 0, text=int(self.student[self.sort_list[index]][0]),
                                    values=(single[0], single[1]))
                app.info.configure(text="INFO: File Loaded.")
                # If the user loaded the file properly, 'Info' Label should shows the message: 'INFO: File Loaded.'

        except (IOError, XLRDError):
            app.info.configure(text="INFO: Loading Failed! Please Try Again.", font=('','7'))
            # If the user did not load the file properly,'Info' Label shows the message: 'INFO: Loading Failed! Please Try Again.'

    def onClick(self, event):
        self.item = app.tree.focus()

    def show_data(self):
        """
        When the users select one student from the student list, and can click on the 'Show Data' button, they can
        see the selected student details. The function inserts the selected students details into 'Student
        Details' Labels on the right. If the users select another student and click 'Show
        Data' button, the contents of the Labels on the right become updated and entries a the
        bottom become populated.
        """
        try:
            app.entry1.delete(0,END)
            app.entry2.delete(0,END)
            app.entry3.delete(0,END)
            app.entry4.delete(0,END)
            app.entry5.delete(0,END)
            self.name=app.tree.item(self.item)['values'][0]+' '+app.tree.item(self.item)['values'][1]
            app.space1.configure(text=app.tree.item(self.item)['values'][0])
            app.space2.configure(text=app.tree.item(self.item)['values'][1])
            app.space3.configure(text=app.tree.item(self.item)['text'])
            app.space4.configure(text=self.student[self.name][3])
            app.space5.configure(text=self.student[self.name][4])
            if self.student[self.name][5] !=  '':
                app.space6.configure(text=int(self.student[self.name][5]))
                app.entry1.insert(0,int(self.student[self.name][5]))
            else:
                app.space6.configure(text=self.student[self.name][5])
                app.entry1.insert(0,self.student[self.name][5])
            if self.student[self.name][6] !=  '':
                app.space7.configure(text=int(self.student[self.name][6]))
                app.entry2.insert(0,int(self.student[self.name][6]))
            else:
                app.space7.configure(text=self.student[self.name][6])
                app.entry2.insert(0,self.student[self.name][6])
            if self.student[self.name][7] !=  '':
                app.space8.configure(text=int(self.student[self.name][7]))
                app.entry3.insert(0,int(self.student[self.name][7]))
            else:
                app.space8.configure(text=self.student[self.name][7])
                app.entry3.insert(0,self.student[self.name][7])
            if self.student[self.name][8] !=  '':
                app.space9.configure(text=int(self.student[self.name][8]))
                app.entry4.insert(0,int(self.student[self.name][8]))
            else:
                app.space9.configure(text=self.student[self.name][8])
                app.entry4.insert(0,self.student[self.name][5])
            if self.student[self.name][9] !=  '':
                app.space10.configure(text=int(self.student[self.name][9]))
                app.entry5.insert(0,int(self.student[self.name][9]))
            else:
                app.space10.configure(text=self.student[self.name][9])
                app.entry5.insert(0,self.student[self.name][9])
        except AttributeError:
            if len(app.tree.get_children()) == 0:
                app.info.configure(text="INFO: Please Load the Files First.", font=('', '7'))
                # If the user pressed on either 'Show Data' button or 'Save Grades' button before loading students list
                # file, 'Info' Label shows the message: 'INFO: Please Load the Files First.'
            else:
                app.info.configure(text="INFO: Please Select A Student First.", font=('', '7'))
                # If the user pressed on 'Show Data' button without selecting a student from the students treeview,
                # 'Info' Label shows the following message: 'INFO: Please Select A Student First.'

class SaveStudentData():

    def __init__(self):
        self.grades=[]

    def save_grades(self):
        """
        After selecting the Student, the user can edit/add grades to the selected student via
        entry widgets below the tree view. After entering the grades, if the user clicks on 'Save Grades'
        button, the entered grades are saved to the data structure that you initially loaded to data
        into from the user selected file. Also, the data shown in 'Student Details' labels are updated instantly
        to display the newly entered grades. For this process we called show data function at the end of this function,
        so program updates the grades.
        """
        try:
            try:
                self.grades.append(int(app.entry1.get()))
                self.grades.append(int(app.entry2.get()))
                self.grades.append(int(app.entry3.get()))
                self.grades.append(int(app.entry4.get()))
                self.grades.append(int(app.entry5.get()))
            except:
                app.info.configure(text='INFO: Warning, The Type of the Grade is incorrect.')
                # If the user pressed on 'Save Grades' with an entry value other than 'int', 'Info' Label shows the message:
                # "INFO: Warning, The Type of the Grade is incorrect."
            number=5
            for index in range(len(self.grades)):
                open_data.student[open_data.name][number] = self.grades[index]
                number += 1
            self.grades=[]
            open_data.show_data()
        except AttributeError:
            if len(app.tree.get_children()) == 0:
                app.info.configure(text="INFO: Please Load the Files First.", font=('', '7'))
                # If the user pressed on the treeview before loading the file, 'Info' Label shows the message:
                # 'INFO: Please Load The Files First.'
        except:
            app.info.configure(text="INFO: Warning, The Type of the Grade is incorrect.", font=('', '7'))
            # If the user enters invalid type, it will give that warning.

    def export_data(self):
        """
        With that function, the user can export and save the grades of the students into a file. First, the
        user chooses a file type by clicking any of the check buttons at the bottom. The available file
        types can be only 'xls', 'csv', and 'txt'.
        Also, there is an entry to specify a name for the file. When user clicks on 'Export Data' button, the program
        saves the grades data  into a file of the selected type and the entered name. The file is saved in the
        current working directory.
        """
        if len(app.entry6.get()) != 0:

            if app.var.get() == 'xls':

                wb = Workbook()
                sheet = wb.add_sheet('Sheet1')
                self.columns = ['id', 'Name', 'Section', 'Dept.', 'Gpa', 'MP1', 'MP2', 'MP3', 'MT', 'FINAL']
                style = xlwt.easyxf('font: bold 1')
                for col in range(10):
                    sheet.write(0, col, self.columns[col], style)
                index=0
                for row in range(1,162):
                    sheet.write(row, 1, open_data.sort_list[index])
                    index += 1
                index1 = -1
                for row in range(1,162):
                    index1 += 1
                    index2=0
                    for col in range(10):
                        if col == 1 or index2 == 1:
                            index2 += 1
                            continue
                        if index2 == 0:
                            sheet.write(row, col, int(open_data.student[open_data.sort_list[index1]][index2]))
                            index2 += 1
                            continue
                        sheet.write(row, col, open_data.student[open_data.sort_list[index1]][index2])
                        index2 += 1
                file_name=app.entry6.get()
                if '.xls' not in file_name:
                    wb.save(file_name+'.xls')
                else:
                    wb.save(file_name)

            elif app.var.get() == 'txt':

                file_name = app.entry6.get()
                if '.txt' not in file_name:
                    file_name = file_name + '.txt'
                file = open(file_name, 'w')
                index2 = 0
                for key in open_data.student:
                    for index in range(10):
                        if index == 0:
                            file.write(str(int(open_data.student[key][index])))
                            file.write(', ')
                            continue
                        if index == 1:
                            try:
                                self.split_names = open_data.sort_list[index2].split(' ')
                                file.write(self.split_names[0])
                                file.write(', ')
                                file.write(self.split_names[1])
                                file.write(', ')
                                index2 += 1
                            except UnicodeEncodeError:
                                index2 += 1
                                pass
                            continue
                        if index >= 5 and index <= 9:
                            if open_data.student[key][index] != '':
                                file.write(str(int(open_data.student[key][index])))
                                file.write(', ')
                            else:
                                file.write('\n')
                                break
                            if index == 9:
                                file.write('\n')
                            continue
                        try:
                            file.write(str(open_data.student[key][index]))
                            file.write(', ')
                        except UnicodeEncodeError:
                            pass
                file.close()



            elif app.var.get() == 'csv':
                app.info.configure(text="INFO: Type not Supported")
                # The program does not support saving in 'csv' type. If the user selects 'csv' file type, 'Info' Label
                # shows the message: 'INFO: Type not Supported'.

            else:
                app.info.configure(text='INFO: Type not chosen!')
                # Also, If the user presses on 'Export Data' button, with a file name provided, but without choosing a
                # file type, 'Info' Label shows the message: 'INFO: Type not chosen'.

        else:
            app.info.configure(text="INFO: Please provide the name of the file.")
            # Also, if the user presses 'Export Data' button without giving a file name, 'Info' Label shows the message:
            # 'INFO: Please provide the name of the file.'



open_data = OpenStudentData()
save = SaveStudentData()
root.title('Grades Management Tool v1.0') #name of the window
root.geometry('880x500+100+100') #sizes of the window
app = Window(root)
root.mainloop()

# references
# https: // knowpapa.com / ttk - treeview /
# https://goo.gl/KPm3Sa
# https://pythonspot.com/tk-file-dialogs/
# https://stackoverflow.com/questions/51561963/how-to-detect-if-treeview-column-is-empty
# https://www.geeksforgeeks.org/writing-excel-sheet-using-python/
# https://xlsxwriter.readthedocs.io/
# https://stackoverflow.com/questions/23600059/check-flask-upload-if-user-does-not-selected-file
# https://stackoverflow.com/questions/41642761/how-to-update-a-label-in-python
# https://python-forum.io/Thread-bind-hover-on-tkinter-ttk-Treeview
# https://www.daniweb.com/programming/software-development/threads/492151/how-to-get-selected-items-in-ttk-treeview
# https://stackoverflow.com/questions/3794268/command-for-clicking-on-the-items-of-a-tkinter-treeview-widget

