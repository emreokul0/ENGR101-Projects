class User:
    def __init__(self,name,balance,phone_number,is_disqualified=False):
        self.name=name
        self.balance=balance
        self.phone=phone_number
        self.is_disqualified=is_disqualified
    def print_user_stats(self):
        print "Name:", self.name,"Balance:", self.balance, "Phone Number:", self.phone

class Answer:
    def __init__(self,text,answer_no,is_correct,num_answering_users):
        self.text=text
        self.answer_no=answer_no
        self.is_correct=is_correct
        self.num_answering_users=num_answering_users
    def display(self,display_answers,display_correctness):
        return self.answer_no

class Question:
    def __init__(self,question_text):
        self.question_text=question_text
        self.answers=[]
        self.correct_ans=None
    def add_answer(self,answer_text,answer_no,is_correct):
        if is_correct == True:
            self.correct_ans=answer_no
        self.answers.append(Answer(answer_text,answer_no,is_correct,0))
    def display(self,display_answers,display_correctness):
        print self.question_text
        for index in range(len(self.answers)):
            print "ans", str(index+1) + ".", self.answers[index].text,
            if display_correctness == True:
                print self.answers[index].is_correct,
            if display_answers == True:
                print self.answers[index].num_answering_users,
            print
    def process_answers(self,user,current_user,index):
        import random
        game.players_in_game=user
        game.current_user=current_user
        print "\n************************* Total Players: " + str(len(game.players_in_game))
        print "\n--- Q" + str(index + 1) + ":",
        game.question_objects[index].display(False, False)
        if game.user_objects[int(game.sign_in)].is_disqualified == False:
            while True:  # This checks whether or not user gives a valid answer.
                user_answer = raw_input("\nYour answer: ")
                if user_answer == "":
                    print "\nYour answer cannot be empty!"
                elif int(user_answer) != 1 and int(user_answer) != 2 and int(user_answer) != 3:
                    print "\nPlease choose 1 or 2 or 3!"
                else:
                    break
            user_answer = int(user_answer)
            if user_answer == 1:
                game.question_objects[index].answers[0].num_answering_users += 1
            if user_answer == 2:
                game.question_objects[index].answers[1].num_answering_users += 1
            if user_answer == 3:
                game.question_objects[index].answers[2].num_answering_users += 1
            if False == game.question_objects[index].answers[user_answer - 1].is_correct:
                game.user_objects[int(game.sign_in)].is_disqualified = True
                print "\nIncorrect! :("
            else:
                print "\nCorrect! :)"
        for key, player in game.players_in_game.items():  # This counts "players in game"'s keys.
            bot_answer = random.randint(1, 3)
            if bot_answer == 1:
                game.question_objects[index].answers[0].num_answering_users += 1
            if bot_answer == 2:
                game.question_objects[index].answers[1].num_answering_users += 1
            if bot_answer == 3:
                game.question_objects[index].answers[2].num_answering_users += 1
            if game.question_objects[index].answers[bot_answer - 1].is_correct == False:
                player.is_disqualified = True
                game.loser_players.append(key)
        print "\nEvaluating the responses of the other competitors....\n"
        print "\n--- Q" + str(index + 1) + ":",
        game.question_objects[index].display(True, True)
        for loser in game.loser_players:
            del game.players_in_game[loser]

class Menu:
    def __init__(self,header):
        self.menu_item=[]
        self.header=header
    def display(self,display_header):
        if display_header == True:
            print self.header
        for item in self.menu_item:
            item.display()
    def add_menu_item(self,text,number):
        self.menu_item.append(MenuItem(text,number))

class MenuItem:
    def __init__(self,text,number):
        self.text=text
        self.number=number
    def display(self):
        print str(self.number), "-", self.text

class Game:
    def __init__(self,prize=10000.0):
        self.question_objects=[]
        questions = {1: {"Question": "What color are Zebras?",
                         1: ("White with black stripes", True),
                         2: ("Black with white stripes", False),
                         3: ("Black with red stripes", False)},
                     2: {"Question": "Where was the old Campus of Sehir University?",
                         1: ("Levent", False),
                         2: ("Altunizade", True),
                         3: ("Maltepe", False)}}
        for question_number in questions:
            self.question_objects.append(Question(questions[question_number]["Question"]))
            self.question_objects[len(self.question_objects)-1].add_answer(questions[question_number][1][0],1,
                                                                      questions[question_number][1][1])
            self.question_objects[len(self.question_objects)-1].add_answer(questions[question_number][2][0],2,
                                                                      questions[question_number][2][1])
            self.question_objects[len(self.question_objects)-1].add_answer(questions[question_number][3][0],3,
                                                                      questions[question_number][3][1])
        self.admin_menu=Menu("\nWelcome Sehir Hadi Admin Section, please choose one of the following options:\n")
        self.prize=prize
        self.build_admin_menu()
    def play(self):
        self.user_objects={}
        players = {5577: ["emre", 5.4], 5547: ["mustafa", 3.2],
                   5551: ["enes", 6.4], 5334: ["murat", 10.2],
                   5366: ["umran", 999.2], 5535: ["atamert", 3.5],
                   5834: ["anil", 6.3]}
        for key in players:
            self.user_objects[key] = User(players[key][0], players[key][1], key)
        while True:
            self.__init__(10000.0)
            self.login()
            self.user_objects[int(self.sign_in)].is_disqualified=False
            self.players_in_game = {}
            for player in self.user_objects.values():
                self.players_in_game[player.phone] = player
            del self.players_in_game[int(self.sign_in)]
            for index in range(len(self.question_objects)):
                self.loser_players = []
                self.question_objects[index].process_answers(self.players_in_game,self.user_objects[int(self.sign_in)],index)
            if self.user_objects[int(self.sign_in)].is_disqualified == False:
                self.players_in_game[int(self.sign_in)] = self.user_objects[int(self.sign_in)]
            if len(self.players_in_game) != 0:
                self.distribute_prize()
            else:
                print """
Oh, no one??
Next Time :((("""

    def build_admin_menu(self):
        list = ["Set prize for the next competition.",
                "Display questions for the next competition.",
                "Add new question to the next competition.",
                "Delete a question from the next competition.",
                "See users' data.",
                "Log out."]
        for index in range(len(list)):
            self.admin_menu.add_menu_item(list[index], index + 1)
    def show_admin_menu(self):
        while True:
            self.admin_menu.display(True)
            menu_number = raw_input("\nPlease enter a menu number: ")
            if menu_number == "" or int(menu_number)>6 or int(menu_number)<=0:  # This will warn user if user enter an empty space.
                print "\nPlease enter a valid number!"
                continue
            if menu_number=="1":
                while True:
                    total_prize = raw_input("\nPlease type the total prize of the next competition: ")
                    if total_prize == "":
                        print "\nPlease enter a valid prize!"
                        continue
                    print "\n" + total_prize
                    self.prize=float(total_prize)
                    print "\nSetting prize..."
                    break
            if menu_number=="2":
                for index in range(len(self.question_objects)):
                    print "\n--- Q" + str(index+1) + ":",
                    self.question_objects[index].display(False,True)
            if menu_number=="3":
                while True:
                    add_question = raw_input("\nPlease type the question: ")
                    answer1 = raw_input("Please type the CORRECT answer: ")
                    answer2 = raw_input("Please type an incorrect answer: ")
                    answer3 = raw_input("Please type an incorrect answer: ")
                    if add_question == "" or answer1 == "" or answer2 == "" or answer3 == "":
                        print "\nYou cannot leave any of them empty!"
                    else:
                        break
                self.question_objects.append(Question(add_question))
                self.question_objects[len(self.question_objects) - 1].add_answer(answer1, 1,
                                                                                 True)
                self.question_objects[len(self.question_objects) - 1].add_answer(answer2, 2,
                                                                                 False)
                self.question_objects[len(self.question_objects) - 1].add_answer(answer3, 3,
                                                                                 False)
                print """
Adding to the questions database.....
Done..."""
            if menu_number=="4":
                for index in range(len(self.question_objects)):
                    print "\n--- Q" + str(index+1) + ":", self.question_objects[index].question_text
                delete_question = raw_input("\nPlease type the number of the question to be deleted: ")
                delete_question = int(delete_question)-1
                while delete_question+1 < len(self.question_objects):
                    self.question_objects[delete_question] = self.question_objects[delete_question + 1]
                    delete_question += 1
                del self.question_objects[delete_question]
                print "Q" + str(delete_question), "has been deleted successfully!"
            if menu_number=="5":
                for player in self.user_objects.values():
                    player.print_user_stats()
            if menu_number=="6":
                break
    def distribute_prize(self):
        print "\n--- Total Winners =", str(len(self.players_in_game))
        print "--- Total Distributed Prize =", str(self.prize) + "\n"
        self.prize/=len(self.players_in_game)
        for winners in self.players_in_game.values():
            winners.balance += self.prize
            print winners.name, "=", self.prize, "---->", "Total Balance =", winners.balance
        print "\nSee you later..."
    def login(self):
        while True:
            print "\n--- Welcome to Sehir Hadi :) ---"
            self.sign_in = raw_input("\nPlease type your phone number in order to sign in: ")
            if self.sign_in == "**":
                self.show_admin_menu()
            elif self.sign_in == "":  # If user enters an empty space for sign in, user will get a warn.
                print "\n" + "You cannot leave that empty, please try again!"
            else:
                print "\nChecking", self.sign_in + "...."
                is_user_real=False
                for user in self.user_objects.values():
                    if user.phone == int(self.sign_in):
                        is_user_real=True
                        print "Welcome", self.user_objects[int(self.sign_in)].name
                        print "Competition will start soon... Be ready :)"
                        break
                if is_user_real == True:
                    break
game=Game()
game.play()