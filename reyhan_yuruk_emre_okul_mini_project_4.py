from Tkinter import *
from ttk import Combobox
from bs4 import BeautifulSoup
import urllib2
from mysearchengine import *
import ttk
root = Tk()

class Window(Frame):

    def __init__(self,parent):

        Frame.__init__(self,parent)
        self.controller = 0
        self.searcher = Searcher()
        self.initUI()

    def initUI(self):

        self.pack(fill=X)

        self.caption = Label(self, text='Classroom Finder', bg='dodgerblue',
                             fg='white', font=('', '28', 'bold'), height=1)
        self.caption.pack(fill=X)

        self.frame_1 = Frame(self)
        self.frame_1.pack(pady=(20,30))

        self.url_label = Label(self.frame_1, text='Url:')
        self.url_label.grid(row=0, column=0, sticky=W, padx=(0,15))

        self.url_entry = Entry(self.frame_1, width=165)
        self.url_entry.grid(row=0, column=1, sticky=NSEW, ipady=2, padx=(0,10))
        self.url_entry.insert(END, 'https://www.sehir.edu.tr/tr/duyurular/2018-2019-bahar-donemi-ders-programi')

        self.frame_2 = Frame(self)
        self.frame_2.pack(pady=(0,40))

        self.fetch_button = Button(self.frame_2, text='Fetch', command=self.fetch_button, width=10,  height=2)
        self.fetch_button.pack(side=RIGHT)

        self.color_label = Label(self.frame_2, bg='red', width=10)
        self.color_label.pack(side=RIGHT, padx=(880,10))

        self.frame_3 = Frame(self)
        self.frame_3.pack()

        self.filters_label = Label(self.frame_3, text='Filters', bg='dodgerblue',
                                   fg='white', font=('', '25', 'bold'), height=1)
        self.filters_label.pack(side=LEFT, padx=(0,970))

        self.frame_4 = Frame(self, borderwidth=2, relief=RIDGE)
        self.frame_4.pack(fill=BOTH, padx=12, pady=(10,0))

        self.frame_5 = Frame(self.frame_4)
        self.frame_5.grid(row=0, column=0, sticky=NSEW)

        self.where_label = Label(self.frame_5, text='Where am I?')
        self.where_label.grid(row=0, column=0, sticky=W, padx=25, pady=(20,10))

        self.room_label = Label(self.frame_5, text='Room')
        self.room_label.grid(row=1, column=0, sticky=W, padx=25, pady=10)

        self.start_label = Label(self.frame_5, text='Start')
        self.start_label.grid(row=2, column=0, sticky=W, padx=25, pady=10)

        self.day_label = Label(self.frame_5, text='Day')
        self.day_label.grid(row=3, column=0, sticky=W, padx=25, pady=10)

        self.search_button = Button(self.frame_5, text='Search', command=self.search_button)
        self.search_button.grid(row=4, column=0, sticky=EW, padx=25, pady=10)

        self.where_combobox = Combobox(self.frame_5, state='readonly')
        self.where_combobox.grid(row=0, column=1, columnspan=2, padx=(25,0), pady=(15,0))

        self.room_combobox = Combobox(self.frame_5, state='readonly')
        self.room_combobox.grid(row=1, column=1, columnspan=2, padx=(25,0))

        self.start_combobox = Combobox(self.frame_5, state='readonly', width=7)
        self.start_combobox.grid(row=2, column=1, padx=(25,0), sticky=W)

        self.end_label = Label(self.frame_5, text='End')
        self.end_label.grid(row=2, column=2)

        self.end_combobox = Combobox(self.frame_5, state='readonly', width=7)
        self.end_combobox.grid(row=2, column=3, padx=(30,20))

        self.day_combobox = Combobox(self.frame_5, state='readonly')
        self.day_combobox.grid(row=3, column=1, columnspan=2, padx=(25,0))

        self.frame_6 = Frame(self.frame_4, borderwidth=2, relief=RIDGE)
        self.frame_6.grid(row=0, column=1, sticky=NSEW, padx=20, pady=10)

        self.classroom_results_label = Label(self.frame_6, text='Clasroom Results', bg='lightblue4', fg='white')
        self.classroom_results_label.grid(row=0, column=0, columnspan=2, sticky=EW)

        self.scrollbar = Scrollbar(self.frame_6)
        self.tree = ttk.Treeview(self.frame_6, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree['columns'] = ('#0','#1','#2','#3')
        self.tree.column('#0',width=100)
        self.tree.column('#1',width=100)
        self.tree.column('#2',width=100)
        self.tree.column('#3',width=100)
        self.tree.column('#4',width=100)
        self.tree.heading('#0',text='Room')
        self.tree.heading('#1',text='Traffic')
        self.tree.heading('#2',text='Availability%')
        self.tree.heading('#3',text='Closeness')
        self.tree.heading('#4',text='Overall Score')
        self.tree.grid(row=1, column=0, sticky=E, padx=(10,0), pady=10, ipadx=45, ipady=20)
        self.scrollbar.grid(row=1, column=1, sticky=N+S+W, padx=(0,10), pady=10)

    def fetch_button(self):

        if self.controller == 0:

            self.color_label.config(bg='yellow')

            self.update_idletasks()

            self.searcher.fetch()

            self.color_label.config(bg='green')
            self.controller += 1

            self.sorted_builds = sorted(self.searcher.build_and_class)
            self.where_combobox.config(state='readonly', values=[build_no for build_no in self.sorted_builds])
            self.where_combobox.current(0)
            self.room_combobox.config(state='readonly', values=[str(room)[1:] for room in self.searcher.build_and_class[self.where_combobox.get()]])
            self.room_combobox.current(0)

            self.all_times = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
            self.start_combobox.config(state='readonly', values=self.all_times[:len(self.all_times)-1])
            self.start_combobox.current(0)
            self.end_combobox.config(state='readonly', values=self.all_times[1:])
            self.end_combobox.current(len(self.all_times)-2)

            self.day_combobox.config(state='readonly', values=['Monday','Tuesday','Wednesday','Thursday','Friday'])
            self.day_combobox.current(0)

            self.searcher.compute_traffic_scores()

            self.searcher.compute_closeness_scores()

            self.searcher.compute_availability_scores()

    def search_button(self):

        self.searcher.search(Day(self.day_combobox.get()),
                             Classroom(self.where_combobox.get()[-1], self.room_combobox.get()[0],
                                       self.room_combobox.get()[1:]))

class Classroom():

    def __init__(self,building_number,floor_number,room_number):

        self.building_number = building_number
        self.floor_number = floor_number
        self.room_number = room_number
        self.traffic_score = {}

    def get_distance_from(self):
        pass

class Building():

    def __init__(self,name):

        self.name = name
        self.classrooms = [] # Classroom objects sorted by room number

class Day():

    def __init__(self,name):

        self.name = name
        self.time_slots = {}

class SearchResultItem():

    def __init__(self,availability_score,closeness_score,available_slots):

        self.classroom = Classroom
        self.availability_score = availability_score
        self.closeness_score = closeness_score
        self.available_slots = available_slots

    def compute_availability_score(self,start_time,end_time):
        pass

class Searcher():

    def __init__(self):

        self.days = {}
        self.buildings = {}

    def fetch(self):

        page = app.url_entry.get()
        soup = BeautifulSoup(urllib2.urlopen((page)).read(), 'html.parser')

        all = []
        for i in soup.find_all('tbody'):
            for j in i.find_all('tr'):
                temp = []
                for z in j:
                    temp.append(z.text.split())
                all.append(temp)

        self.course_schedules = {}
        self.build_and_class = {}
        self.class_list = []

        for i in all[1:]:

            if 'ACAD BUILD KEMAL KARPAT' in ' '.join(i[4]) or ' '.join(i[0]) == '' or ' '.join(i[1]) == '' or ' '.join(
                    i[2]) == '' or \
                    ' '.join(i[3]) == '' or ' '.join(i[4]) == '' or ' '.join(i[5]) == '' or 'Saturday' in ' '.join(
                i[2]) or 'ACAD' not in ' '.join(i[4]):
                continue

            day = str(' '.join(i[2]))  # Course Days
            time = str(' '.join(i[3]))  # Course Times
            place = str(' '.join(i[4])).split(' #')  # Course Place
            if '20:00' in time:
                time = time.strip('20:00') + '19:00'
            if '21:00' in time:
                time = time.split('2')[0] + '19:00'
            if '21:30' in time:
                time = time.split('2')[0] + '19:00'
            if '22:00' in time:
                time = time.strip('22:00') + '19:00'
            if 'LAB' in ' '.join(i[4]):
                place = place[0] + place[1].strip(' LAB BUILD 1')
            if 'LAB' not in ' '.join(i[4]) and len(place) != 2:
                build = place[0]
                class_no = place[1].split()[0]
                index = 0
                while index < 2:

                    self.build_and_class.setdefault(build, 0)
                    if int(class_no) not in self.class_list:
                        self.class_list.append(int(class_no))
                    self.course_schedules.setdefault(day.split()[index], {})
                    self.course_schedules[day.split()[index]].setdefault(class_no, [])

                    if time.split()[index] in self.course_schedules[day.split()[index]][class_no]:
                        continue
                    else:
                        self.course_schedules[day.split()[index]][class_no].append(time.split()[index])

                    build = ' '.join(place[1].split()[1:])
                    class_no = place[2]
                    index += 1

            else:

                if place[0] == 'A':
                    continue
                self.build_and_class.setdefault(place[0], 0)
                if place[1] == 'C':
                    continue
                if int(place[1]) not in self.class_list:
                    self.class_list.append(int(place[1]))

                if len(time.split()) != 1 and len(day.split()) != 1:
                    for index in range(len(time.split())):
                        self.course_schedules.setdefault(day.split()[index], {})
                        self.course_schedules[day.split()[index]].setdefault(place[1], [])
                        if time.split()[index] in self.course_schedules[day.split()[index]][place[1]]:
                            continue
                        else:
                            self.course_schedules[day.split()[index]][place[1]].append(time.split()[index])
                elif len(time.split()) == 1 and len(day.split()) != 1:
                    for index in range(len(day.split())):
                        self.course_schedules.setdefault(day.split()[index], {})
                        self.course_schedules[day.split()[index]].setdefault(place[1], [])
                        if time in self.course_schedules[day.split()[index]][place[1]]:
                            continue
                        else:
                            self.course_schedules[day.split()[index]][place[1]].append(time)
                elif len(time.split()) != 1 and len(day.split()) == 1:
                    for index in range(len(time.split())):
                        self.course_schedules.setdefault(day, {})
                        self.course_schedules[day].setdefault(place[1], [])
                        if time.split()[index] in self.course_schedules[day][place[1]]:
                            continue
                        else:
                            self.course_schedules[day][place[1]].append(time.split()[index])
                else:
                    self.course_schedules.setdefault(day, {})
                    self.course_schedules[day].setdefault(place[1], [])
                    if time in self.course_schedules[day][place[1]]:
                        continue
                    else:
                        self.course_schedules[day][place[1]].append(time)

        for build_no in self.build_and_class:
            temp = []
            for class_number in self.class_list:
                if str(class_number).startswith(build_no.split()[-1]):
                    temp.append(class_number)
            self.build_and_class[build_no] = sorted(temp)

        for build_no in self.build_and_class:
            for class_no in self.build_and_class[build_no]:
                class_no = str(class_no)
                classroom = Classroom(class_no[0],class_no[1],class_no[2:])
                self.buildings.setdefault(class_no,Building(class_no))
                self.buildings[class_no].classrooms.append(classroom)

    def compute_availability_scores(self):

        self.availability_score_dict = {}
        self.available_slots_dict = {}
        for day_name in self.course_schedules:
            self.availability_score_dict.setdefault(day_name,{})
            for class_no in self.course_schedules[day_name]:
                self.availability_score_dict[day_name].setdefault(class_no,0)
                busy_hours = 0
                self.times = []
                self.start_interval = int(app.start_combobox.get()[:2])
                self.end_interval = int(app.end_combobox.get()[:2])
                for step in range(self.end_interval - self.start_interval):
                    self.times.append(str(self.start_interval + step) + ':00')
                for time in self.course_schedules[day_name][class_no]:
                    start_hour = int(time.split('-')[0][:2])
                    end_hour = int(time.split('-')[1][:2])
                    hour_list = [hour for hour in range(start_hour,end_hour)]
                    for time_interval in range(self.start_interval,self.end_interval):
                        if time_interval not in hour_list:
                            if str(time_interval)+':00' not in self.times:
                                continue
                            else:
                                self.times.remove(str(time_interval)+':00')
                        else:
                            if str(start_hour) + ':30' == '18:30':
                                busy_hours += 0.5
                            else:
                                busy_hours += 1
                if busy_hours == self.end_interval-self.start_interval:
                    self.availability_percent = 0
                elif busy_hours == 0:
                    self.availability_percent = 100
                else:
                    minutes_for_interval = (self.end_interval-self.start_interval) * 60
                    minutes_for_busy = ((self.end_interval-self.start_interval)-busy_hours) * 60
                    self.availability_percent = 100 * minutes_for_busy / minutes_for_interval
                self.availability_score_dict[day_name][class_no] = self.availability_percent
                if len(self.times) != 0:
                    self.days.setdefault(day_name, Day(day_name))
                    self.all_times = []
                    for step in range(self.end_interval - self.start_interval):
                        self.all_times.append(str(self.start_interval + step) + ':00')
                    for hour_slice in self.all_times:
                        if hour_slice in self.times:
                            classroom = Classroom(class_no[0], class_no[1], class_no[2:])
                            self.days[day_name].time_slots.setdefault(hour_slice, [])
                            self.days[day_name].time_slots[hour_slice] = classroom
                        else:
                            self.available_slots_dict.setdefault(day_name, {})
                            self.available_slots_dict[day_name].setdefault(class_no, [])
                            self.available_slots_dict[day_name][class_no].append(hour_slice)
        for build_no in self.build_and_class:
            for other_class in self.build_and_class[build_no]:
                for day_name in self.availability_score_dict:
                    if str(other_class) not in self.availability_score_dict[day_name]:
                        self.availability_percent = 100
                        self.availability_score_dict[day_name].setdefault(str(other_class), 0)
                        self.availability_score_dict[day_name][str(other_class)] = self.availability_percent
        self.normalize_availability_score_dict = {}
        for day_name in self.availability_score_dict:
            a_s = normalizescores(self.availability_score_dict[day_name],smallIsBetter=False)
            self.normalize_availability_score_dict.setdefault(day_name,a_s)
        return self.normalize_availability_score_dict

    def compute_traffic_scores(self):

        self.traffic_scores_dict = {}
        for day_name in self.course_schedules:
            self.traffic_scores_dict.setdefault(day_name,{})
            for class_no in self.course_schedules[day_name]:
                self.traffic_scores_dict[day_name].setdefault(class_no,0)
                total_hours = 0
                for time in self.course_schedules[day_name][class_no]:
                    start_hour = time.split('-')[0].split(':')[0]
                    end_hour = time.split('-')[1].split(':')[0]
                    delta_time = int(end_hour) - int(start_hour)
                    if time.split('-')[0] == '19:00':
                        continue
                    total_hours += delta_time
                traffic_score = total_hours / float(int(app.end_combobox.get().split(':')[0]) - int(app.start_combobox.get().split(':')[0]))
                self.traffic_scores_dict[day_name][class_no] = traffic_score
        for build_no in self.build_and_class:
            for other_class in self.build_and_class[build_no]:
                for day_name in self.traffic_scores_dict:
                    if str(other_class) not in self.traffic_scores_dict[day_name]:
                        traffic_score = 0.1
                        self.traffic_scores_dict[day_name].setdefault(str(other_class),[])
                        self.traffic_scores_dict[day_name][str(other_class)] = traffic_score
        self.normalize_traffic_score_dict = {}
        for day_name in self.traffic_scores_dict:
            t_s = normalizescores(self.traffic_scores_dict[day_name],smallIsBetter=True)
            self.normalize_traffic_score_dict.setdefault(day_name,t_s)
        return self.normalize_traffic_score_dict

    def compute_closeness_scores(self):

        self.closeness_score_dict = {}
        self.building_current = int(app.where_combobox.get()[-1])
        self.floor_current = int(app.room_combobox.get()[0])
        self.room_current = int(app.room_combobox.get()[1:])
        for build_no in self.build_and_class:
            for room_no in self.build_and_class[build_no]:
                self.building_target = int(str(room_no)[0])
                self.floor_target = int(str(room_no)[1])
                self.room_target = int(str(room_no)[2:])
                self.building_score = abs(self.building_target - self.building_current) * 100
                self.floor_score = abs(self.floor_target - self.floor_current) * 200
                self.room_score = abs(self.room_target - self.room_current) * 50
                self.closeness_score = self.building_score + self.floor_score + self.room_score
                if self.closeness_score == 0:
                    self.closeness_score = 100
                for day_name in self.course_schedules:
                    self.closeness_score_dict.setdefault(day_name,{})
                    self.closeness_score_dict[day_name].setdefault(str(room_no),0)
                    self.closeness_score_dict[day_name][str(room_no)] = self.closeness_score
        self.normalize_closeness_score_dict = {}
        for day_name in self.closeness_score_dict:
            c_s = normalizescores(self.closeness_score_dict[day_name],smallIsBetter=True)
            self.normalize_closeness_score_dict.setdefault(day_name,c_s)
        return self.normalize_closeness_score_dict

    def search(self, day, classroom):

        app.where_combobox.config(state='readonly', values=[build_no for build_no in app.sorted_builds])
        app.where_combobox.current(0)
        app.room_combobox.config(state='readonly', values=[str(room)[1:] for room in
                                                            self.build_and_class[app.where_combobox.get()]])
        app.room_combobox.current(0)

        self.all_dict = {}
        self.list = []
        self.sorted_list = []
        for build_no in self.build_and_class:
            for room_no in self.build_and_class[build_no]:
                room_no = str(room_no)
                self.all_dict.setdefault(day.name,{})
                overall_score = round(self.normalize_traffic_score_dict[day.name][room_no],4)+round(self.normalize_availability_score_dict[day.name][room_no],4)+round(self.normalize_closeness_score_dict[day.name][room_no],4)
                self.list.append(overall_score)
                self.sorted_list = sorted(self.list)
                self.all_dict[day.name].setdefault(overall_score,{})
                for i in ['Room','Traffic','Availability','Closeness']:
                    if i == 'Room':
                        self.all_dict[day.name][overall_score].setdefault(i,room_no)
                    elif i == 'Traffic':
                        self.all_dict[day.name][overall_score].setdefault(i,round(self.normalize_traffic_score_dict[day.name][room_no],4))
                    elif i == 'Availability':
                        self.all_dict[day.name][overall_score].setdefault(i,round(self.normalize_availability_score_dict[day.name][room_no],4))
                    else:
                        self.all_dict[day.name][overall_score].setdefault(i,round(self.normalize_closeness_score_dict[day.name][room_no],4))
        for o_s in self.sorted_list:
            app.tree.insert("", 0, text=self.all_dict[day.name][o_s]['Room'], values=(self.all_dict[day.name][o_s]['Traffic'],self.all_dict[day.name][o_s]['Availability'],self.all_dict[day.name][o_s]['Closeness'],o_s))


root.title('tk')
root.geometry('1100x600+100+80')
app = Window(root)
root.mainloop()