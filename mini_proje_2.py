import random

questions = {1:{"Question":"What color are Zebras?",
                1:("White with black stripes",True),
                2:("Black with white stripes",False),
                3:("Black with red stripes",False)},
             2:{"Question":"Where was the old Campus of Sehir University?",
                1:("Levent",False),
                2:("Altunizade",True),
                3:("Maltepe",False)}}

players = {5577:["emre",5.4],5547:["mustafa",3.2],
           5551:["enes",6.4],5334:["murat",10.2],
           5366:["umran",999.2],5535:["atamert",3.5],
           5834:["anil",6.3]}

total_prize=10000

admin_menu = """
Welcome Sehir Hadi Admin Section, please choose one of the following options:

1 - Set prize for the next competition.
2 - Display questions for the next competition.
3 - Add new question to the next competition.
4 - Delete a question from the next competition.
5 - See users' data.
6 - Log out.
        """
while True:
    while True: # This lets user to sign in.
        print "\n--- Welcome to Sehir Hadi :) ---"
        sign_in = raw_input("\nPlease type your phone number in order to sign in: ")

        if sign_in == "**": # This checks whether or not you want to access to the admin menu.
            while True:
                print admin_menu
                menu_number = raw_input("\nPlease enter a menu number: ")
                if menu_number == "": # This will warn user if user enter an empty space.
                    print "\nPlease enter a valid number!"
                    continue
                elif int(menu_number) == 1: # If user enters 1 for menu number, user can indicate total prize for the game.
                    while True:
                        total_prize = raw_input("\nPlease type the total prize of the next competition: ")
                        if total_prize == "":
                            print "\nPlease enter a valid prize!"
                            continue
                        print "\n" + total_prize
                        print "\nSetting prize..."
                        break

                elif int(menu_number) == 2: # If user enters 2 for menu number, user can see the game questions.
                    question_number = 1
                    while len(questions) >= question_number:
                        print "\n--- Q" + str(question_number) + ":", questions[question_number]["Question"], "---"
                        print "ans 1.", questions[question_number][1][0], ">", questions[question_number][1][1]
                        print "ans 2.", questions[question_number][2][0], ">", questions[question_number][2][1]
                        print "ans 3.", questions[question_number][3][0], ">", questions[question_number][3][1]
                        question_number += 1

                elif int(menu_number) == 3: # If user enters 3 for menu number, user can add a new question.
                    while True:
                        add_question = raw_input("\nPlease type the question: ")
                        answer1 = raw_input("Please type the CORRECT answer: ")
                        answer2 = raw_input("Please type an incorrect answer: ")
                        answer3 = raw_input("Please type an incorrect answer: ")
                        if add_question == "" or answer1 == "" or answer2 == "" or answer3 == "":
                            print "\nYou cannot leave any of them empty!"
                        else:
                            break
                    questions[len(questions)+1] = {"Question": add_question, 1: (answer1, True), 2: (answer2, False),
                                                 3: (answer3, False)}
                    print """
Adding to the questions database.....
Done...
                            """

                elif int(menu_number) == 4: # If user enters 4 for menu number, user can delete a question.
                    question_number = 1
                    while len(questions) >= question_number:
                        print "--- Q" + str(question_number) + ":", questions[question_number]["Question"], "---"
                        question_number += 1
                    delete_question = raw_input("\nPlease type the number of the question to be deleted: ")
                    delete_question=int(delete_question)
                    while delete_question<len(questions):
                        questions[delete_question]=questions[delete_question+1]
                        delete_question+=1
                    del questions[int(delete_question)]
                    print "Q" + str(delete_question), "has been deleted successfully!"

                elif int(menu_number) == 5: # If user enters 5 for menu number, user can see all of the players.
                    for phone_number in players:
                        print players[phone_number][0],"phone number:",phone_number,"balance:",players[phone_number][1]

                elif int(menu_number) == 6: # If user enters 6 for menu number, user can return to sign in.
                    break
                else: # If user enters a number different from "1,2,3,4,5,6" for menu number, user will get a warn.
                    print "Please enter a valid menu number!"
                print "Going back to the Admin Menu..."
        elif sign_in == "": # If user enters an empty space for sign in, user will get a warn.
            print "\n" + "You cannot leave that empty, please try again!"
        elif int(sign_in) in players: # This checks user's sign in in players.
            break
        else:
            print "\n" + sign_in,"is not a valid phone number, please try again!"
    print "\nChecking", str(sign_in) + "...."
    print "Welcome", players[int(sign_in)][0]
    print "Competition will start soon... Be ready :)"

    players_in_game={}
    next_round_players_in_game={}
    for player in players: # This exists to add players's keys to "next round players in game".
        next_round_players_in_game[player]=players[player]
    del next_round_players_in_game[int(sign_in)]
    can_user_play=True
    game_question_number=1

    while len(questions) >= game_question_number: # It works until game question number is bigger than the questions' length.
        players_in_game = {}
        for player in next_round_players_in_game: # This adds "next round players in game"'s keys to "players in game".
            players_in_game[player] = next_round_players_in_game[player]
        print "\n************************* Total Players: " + str(len(players_in_game))
        print "--- Q" + str(game_question_number) + ":", questions[game_question_number]["Question"], "---"
        print "ans 1.", questions[game_question_number][1][0]
        print "ans 2.", questions[game_question_number][2][0]
        print "ans 3.", questions[game_question_number][3][0]
        total_answers_1=0
        total_answers_2=0
        total_answers_3=0

        for player in players_in_game: # This counts "players in game"'s keys.
            bot_answer = random.randint(1, 3)
            if bot_answer == 1:
                total_answers_1+=1
            if bot_answer == 2:
                total_answers_2+=1
            if bot_answer == 3:
                total_answers_3+=1
            if questions[game_question_number][bot_answer][1]==False:
                del next_round_players_in_game[player]

        if can_user_play==True:
            while True: # This checks whether or not user gives a valid answer.
                user_answer = raw_input("\nYour answer: ")
                if user_answer == "":
                    print "\nYour answer cannot be empty!"
                elif int(user_answer) != 1 and int(user_answer) != 2 and int(user_answer) != 3:
                    print "\nPlease choose 1 or 2 or 3!"
                else:
                    break
            if user_answer=="1":
                total_answers_1+=1
            if user_answer=="2":
                total_answers_2+=1
            if user_answer=="3":
                total_answers_3+=1
            if False==questions[game_question_number][int(user_answer)][1]:
                can_user_play=False
                print "\nIncorrect! :("
            else:
                print "\nCorrect! :)"
        print "\nEvaluating the responses of the other competitors....\n"
        print "ans 1.", questions[game_question_number][1][0], questions[game_question_number][1][1], "...", "total answers:",total_answers_1
        print "ans 2.", questions[game_question_number][2][0], questions[game_question_number][2][1], "...", "total answers:",total_answers_2
        print "ans 3.", questions[game_question_number][3][0], questions[game_question_number][3][1], "...", "total answers:",total_answers_3
        game_question_number+=1

    if can_user_play==True:
        next_round_players_in_game[sign_in]=players[int(sign_in)]
    if not len(next_round_players_in_game)==0:
        total_distributed_prize=total_prize/float(len(next_round_players_in_game))
    else:
        print """
Oh, no one??
Next Time :((("""
    print "\n--- Total Winners =", str(len(next_round_players_in_game))
    print "--- Total Distributed Prize =", str(total_distributed_prize) + "\n"
    for winners in next_round_players_in_game:
        players[int(winners)][1]+=total_distributed_prize
        print players[int(winners)][0],"=",total_distributed_prize,"---->", "Total Balance =", players[int(winners)][1]
    print "\nSee you later..."