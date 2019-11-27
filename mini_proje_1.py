alphabet = ["q","w","e","r","t","y","u","o","p","a","s","d","f","g","h","j","k","l","i","z","x","c","v","b","n","m"]
def winner(): #This function finds the winner.
    if First_Turtle_Name_Score >= 200: #This checks the First Turtle's Score.
        print "****** Round ", round_number, " ******"
        print First_Turtle_Name.upper(), " score : ", First_Turtle_Name_Score
        print Second_Turtle_Name.upper(), " score : ", Second_Turtle_Name_Score
        print "+++++++++++++++"
        print First_Turtle_Name.upper(), " wins."
        print "+++++++++++++++"
        while True: #This asks user whether or not to play the game again.
            again = raw_input("Do you want to play another round(yes/no)? : ")
            if again != "yes" and again != "no":
                print "Please choose yes or no!"
                continue
            else:
                break
        if again == "yes":
            SEHIR_Turtle_Cup()
        elif again == "no":
            print "Thanks for playing! See you again!"
            exit()
    elif Second_Turtle_Name_Score >= 200: #This checks the Second Turtle's Score.
        print "****** Round ", round_number, " ******"
        print First_Turtle_Name.upper(), " score : ", First_Turtle_Name_Score
        print Second_Turtle_Name.upper(), " score : ", Second_Turtle_Name_Score
        print "+++++++++++++++"
        print Second_Turtle_Name.upper(), " wins."
        print "+++++++++++++++"
        while True:
            again = raw_input("Do you want to play another round(yes/no)? : ")
            if again != "yes" and again != "no":
                print "Please choose yes or no!"
                continue
            else:
                break
        if again == "yes":
            SEHIR_Turtle_Cup()
        elif again == "no":
            print "Thanks for playing! See you again!"
            exit()
import random
from swampy.TurtleWorld import *
def SEHIR_Turtle_Cup(): #This starts the game.
    global world
    world = TurtleWorld()
    global First_Turtle_Name, Second_Turtle_Name
    print "----- First Turtle -----"
    while True: #This checks whether or not user writes the first turtle's name correctly.
        First_Turtle_Name = raw_input("What is the name of first turtle? = ")
        if len(First_Turtle_Name) == 0 or First_Turtle_Name in alphabet:
            print "Name cannot be empty!"
        else:
            break
    while True: #This checks whether or not user writes the first turtle's color correctly.
        First_Turtle_Color = raw_input("Please select a color for your Turtle red-blue-yellow? = ")
        if (First_Turtle_Color != "red") and (First_Turtle_Color != "blue") and (First_Turtle_Color != "yellow"):
            print First_Turtle_Color, " is not a valid color, please select one of red-blue-yellow colors = "
        else:
            break
    print "----- ", First_Turtle_Name.upper(), " IS READY TO GO :) -----"
    print "----- Second Turtle -----"
    while True: #This checks whether or not user writes the second turtle's name correctly.
        Second_Turtle_Name = raw_input("Please type your turtle's name = ")
        if Second_Turtle_Name == First_Turtle_Name:
            print Second_Turtle_Name, " is taken, please choose another name! = "
        elif len(Second_Turtle_Name) == 0:
            print "Name cannot be empty!"
        else:
            break
    while True: #This checks whether or not user writes the second turtle's color correctly.
        Second_Turtle_Color = raw_input("Please select a color for your Turtle red-blue-yellow? = ")
        if (Second_Turtle_Color != "red") and (Second_Turtle_Color != "blue") and (Second_Turtle_Color != "yellow"):
            print Second_Turtle_Color, " is not a valid color, please select one of red-blue-yellow colors = "
        else:
            break
    print "----- ", Second_Turtle_Name.upper(), " IS READY TO GO :) -----"
    First_Turtle = Turtle()
    Second_Turtle = Turtle()
    First_Turtle.set_color(First_Turtle_Color)
    Second_Turtle.set_color(Second_Turtle_Color)
    First_Turtle.x = -150
    First_Turtle.y = 100
    Second_Turtle.x = -150
    Second_Turtle.y = 150
    First_Turtle.draw()
    Second_Turtle.draw()
    global round_number
    def game(round_number,turtle,name): #This starts to play the game.
        global turtle_steps, change
        print "****** Round ", round_number, " ******"
        print First_Turtle_Name.upper(), " score : ", First_Turtle_Name_Score
        print Second_Turtle_Name.upper(), " score : ", Second_Turtle_Name_Score
        print name.upper(), " plays."
        while True:
            turtle_steps = int(raw_input("How many steps would you like to take? : "))
            if turtle_steps > 100:
                print "Please select a number between 0-100 : "
            elif turtle_steps <= 100:
                break
        change = random.randint(1,101)
        if turtle_steps <= change:
            Turtle.set_delay(turtle, 0.00001)
            def stairs(): #This draws a stair.
                fd(turtle,turtle_steps/5)
                lt(turtle,90)
                for i in range(2):
                    fd(turtle,turtle_steps/5)
                    rt(turtle,90)
                    fd(turtle,turtle_steps/5)
                    lt(turtle,90)
                lt(turtle,180)
                for i in range(2):
                    fd(turtle,turtle_steps/5)
                    lt(turtle,90)
                    fd(turtle,turtle_steps/5)
                    rt(turtle,90)
                lt(turtle,90)
            def circle(): #This draws a circle.
                import math
                circumference = math.pi * (turtle_steps / 2)
                lt(turtle,90)
                for i in range(180):
                    fd(turtle, circumference / 180)
                    rt(turtle, 1)
                lt(turtle,90)
            def forward(): #This draws a line.
                fd(turtle,turtle_steps)
            style = random.randint(1,4)
            if style == 1:
                stairs()
            elif style == 2:
                circle()
            elif style == 3:
                forward()
            print "Success :))))"
        else:
            print "Failed :(((("
    global First_Turtle_Name_Score, Second_Turtle_Name_Score
    start_up = random.randint(1,2)
    First_Turtle_Name_Score = 0
    Second_Turtle_Name_Score = 0
    if start_up == 1:
        round_number = 0
        while First_Turtle_Name_Score < 200 and Second_Turtle_Name_Score < 200: #This organizes turtles' turns.
            round_number += 1
            game(round_number,First_Turtle,First_Turtle_Name)
            if turtle_steps <= change:
                First_Turtle_Name_Score+=turtle_steps
                winner()
            game(round_number+1,Second_Turtle,Second_Turtle_Name)
            if turtle_steps <= change:
                Second_Turtle_Name_Score+=turtle_steps
                winner()
            round_number += 1
    elif start_up == 2:
        round_number = 0
        while First_Turtle_Name_Score < 200 and Second_Turtle_Name_Score < 200: #This organizes turtles' turns.
            round_number += 1
            game(round_number,Second_Turtle,Second_Turtle_Name)
            if turtle_steps <= change:
                Second_Turtle_Name_Score += turtle_steps
                winner()
            game(round_number+1,First_Turtle,First_Turtle_Name)
            if turtle_steps <= change:
                First_Turtle_Name_Score += turtle_steps
                winner()
            round_number += 1
SEHIR_Turtle_Cup()