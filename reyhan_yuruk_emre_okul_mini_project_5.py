# Reference list at the bottom

# firstly we called libraries and module in order to use them
import docclass
from Tkinter import *
from bs4 import BeautifulSoup
import urllib2
root = Tk() # we created Tk root which is a window

class Window(Frame):
    # this class builds the graphical user interface of the tool with an attribute that is an object of Predictor class.

    def __init__(self,parent):

        Frame.__init__(self,parent)
        self.predictor = Predictor()
        self.initUI()

    def initUI(self):

        self.pack(fill=X)

        self.caption = Label(self, text='PI Estimator Tool for SEHIR CS Projects', bg='#00A0AF',
                             fg='white', font=('', '25', 'bold'), height=1)
        self.caption.pack(fill=X)

        self.frame_1 = Frame(self)
        self.frame_1.pack(pady=(20,20))

        # there are two entry widgets at the top, the user provides the URLs for the web pages and the first URL lists
        # the Sehir CS faculty members, and the second URL lists the research project details
        self.url_entry_one = Entry(self.frame_1, font=('', '12'), width=95, justify=CENTER)
        self.url_entry_one.grid(row=0, column=1, sticky=NSEW, ipady=2)
        self.url_entry_one.insert(0, 'http://cs.sehir.edu.tr/en/people/')
        # These widgets has the URLs of web pages by default, when the app is launched

        self.url_entry_two = Entry(self.frame_1, font=('', '12'), width=95, justify=CENTER)
        self.url_entry_two.grid(row=1, column=1, sticky=NSEW, ipady=2, pady=(10,15))
        self.url_entry_two.insert(0, 'http://cs.sehir.edu.tr/en/research/')

        self.fetch_button = Button(self.frame_1, text='Fetch', command=self.fetch_button,
                                   font=('', '11', 'bold'), width=10)
        self.fetch_button.grid(row=2, column=1, sticky=NS, ipady=2)

        self.frame_2 = Frame(self)
        self.frame_2.pack(side=LEFT, padx=(130,0))

        self.projects_label = Label(self.frame_2, text='Projects', font=('', '20'))
        self.projects_label.grid(row=0, column=0)

        self.prediction_label = Label(self.frame_2, text='Prediction', font=('', '20'))
        self.prediction_label.grid(row=0, column=1, padx=(80, 0))

        self.predict_name_label = Label(self.frame_2, font=('', '20'))
        self.predict_name_label.grid(row=1, column=1, pady=60, padx=(75,0))

        self.frame_3 = Frame(self.frame_2)
        self.frame_3.grid(row=1, column=0, sticky=NSEW)

        self.scrollbar = Scrollbar(self.frame_3)
        self.listbox = Listbox(self.frame_3, selectmode='single', yscrollcommand=self.scrollbar.set,
                               height=12, width=120)
        self.listbox.bind('<<ListboxSelect>>',self.current)
        self.listbox.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill=Y)

    def current(self, event):

        self.selected = self.listbox.get(self.listbox.curselection())

        self.predictor.predict_PI()

    def fetch_button(self):
        # When the user clicks on fetch button, the program fetches the datas with BeautifulSoup

        self.page_1 = self.url_entry_one.get()
        self.page_2 = self.url_entry_two.get()
        # from the first link, program collects the links to the profile pages of CS faculty members
        self.soup_1 = BeautifulSoup(urllib2.urlopen((self.page_1)).read(), 'html.parser')
        # from the second link, program fetches the research projects detail
        self.soup_2 = BeautifulSoup(urllib2.urlopen((self.page_2)).read(), 'html.parser')

        self.profile_links = []

        for i in self.soup_1.find_all('a'):
            j = i.get('href')
            if '/en/profile' in str(j):
                if str(j) not in self.profile_links:
                    self.profile_links.append(j)

        self.predictor.fetch_members(self.page_1, self.profile_links)

        self.predictor.fetch_projects(self.page_2, self.soup_2)

class FacultyMember():

    def __init__(self, name, profile_url):

        self.name = name
        self.profile_url = profile_url
        self.publications = []

class ResearchProject():

    def __init__(self, title, summary, PI_name):

        self.title = title
        self.summary = summary
        self.PI_name = PI_name

class Predictor():

    def __init__(self):

        # a Naive Bayes object is created
        self.classifier = docclass.naivebayes(docclass.getwords)
        self.faculty_members = {}
        # a dictionary where keys are faculty member name, values are the corresponding faculty member object
        self.projects = {}
        # a dictionary where keys are project title, values are the corresponding research project object

    def fetch_members(self, page, links):

        self.PI_names = []

        for link in links:
            link = str(link)
            full_link = page.strip('/en/people/') + link
            # it goes to the profile of each faculty member,
            # and collects the faculty member's first and last name and the publication information
            link_soup = BeautifulSoup(urllib2.urlopen((full_link)).read(),'html.parser')
            for member in link_soup.find_all('h3'):
                member_name = ' '.join(member.text.strip().split())
                if len(member.text.strip().split()) == 3: # it ignores the middle names
                    member_name = member.text.strip().split()[0] + ' ' + member.text.strip().split()[-1]
                self.facultymember = FacultyMember(member_name,full_link)
                self.fetch_publications(page, link_soup, link)

    def fetch_publications(self, page, soup, link):

        for i in soup.find_all('div'):
            if i.get('id') == 'flat':
                for j in i.find_all('ul'):
                    for k in j.find_all('li'):
                        text = k.text.strip().split()
                        if 'Citation' in k.text:
                            del text[-2:]
                            self.facultymember.publications.append(' '.join(text[1:len(text)]))
                            continue
                        self.facultymember.publications.append(' '.join(text[1:len(text)]))
        self.faculty_members.setdefault(self.facultymember.name, self.facultymember)
        self.PI_names.append(self.facultymember.name)

    def fetch_projects(self, page, soup):

        self.project_names = []
        # it fetch the title, principal investigator, and summary for each research project
        for i in soup.find_all('li', attrs={'class': 'list-group-item'}):
            title = i.find('h4').text.strip()
            PI_name = i.find_all('a')[1].text.strip()
            sum = i.find('p', attrs={'class': 'gap'}).text.strip()
            # It ignores the projects whose principal investigator is not included in the first URL,
            # as these projects were carried out by ex-faculty members
            if PI_name in self.PI_names:
                researchproject = ResearchProject(title,sum,PI_name)
                self.projects.setdefault(researchproject.title, researchproject)
                self.project_names.append(researchproject.title)
        # when data fetching is completed, the listbox is populated with the fetched research project titles,
        # sorted in alphabetical order.
        for project_name in sorted(self.project_names):
            app.listbox.insert(END, project_name)
        self.train_classifier()

    def train_classifier(self):
        # publications of CS faculty members is trained by the Naive Bayes object which is train function
        for PI_name in self.PI_names:
            for publication in self.faculty_members[PI_name].publications:
                self.classifier.train(publication, PI_name)

    def predict_PI(self):
        # the predicted PI name is shown in a label on the right, if the prediction is correct, the PI name label
        # will have a green background, if it is not correct, the background color of the PI label is red

        for project_title in self.projects:
            if app.selected == project_title:
                item = project_title + ' ' + self.projects[project_title].summary
                # predicted name is taken by the Naive Bayes object which is classify function
                predicted_PI_name = self.classifier.classify(item)
                if predicted_PI_name == self.projects[project_title].PI_name:
                    app.predict_name_label.config(text=predicted_PI_name, bg='green')
                else:
                    app.predict_name_label.config(text=predicted_PI_name, bg='red')

root.title('PI Estimator Tool for SEHIR CS Projects') # name of the window
root.geometry('1200x500+100+80') # sizes of the window
app = Window(root)
root.mainloop()

# reference
# https://stackoverflow.com/questions/14386113/python-ttk-entry-how-to-center-the-input

