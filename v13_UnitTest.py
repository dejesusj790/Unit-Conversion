import random
import math
import sys
import sigfig2
from tkinter import *
import tkinter.messagebox

#Ideas:
#   1. Complex units could be classes, like a class for gas units, temp units, this would allow for randomness to pick units from the same class so don't have like atm -> Kelvin
#   2. Put a entry for how many quetions the user wants to print into text, right now it's default to 10
#   3. Make a button to show how the user should input their answer with value+space+unit (i.e. 1.2 mL)

class Format:
    """This contians methods that will help modify the correct_ans as needed"""
    def amount_sigfig(start_value,start_units,end_units):
        solve={"atm|kPa":101.325,"kPa|atm":0.00986923, "torr|atm":0.00131579,
                "atm|torr":760,"kPa|torr":7.50062,"torr|kPa":0.133322,
                "Celsius|Kelvin":273.15,"Kelvin|Celsius":-273.15}
        key=start_units+"|"+end_units
        start_len=Format.determine_sigfig(start_value)
        oper_len=Format.determine_sigfig(solve[key])
        sigfig_value=min(start_len,oper_len)
        return sigfig_value
    def format_e(correct_ans,n):
        conversion_string="%."+str(n)+"E"
        correct_ans=conversion_string%correct_ans
        return correct_ans
    def sci_not(correct_ans,n,sigfig=False):
        correct_ans_len=len(str(correct_ans))
        sig_example_dict={1:"1E-9",2:"1.2E-9",3:"1.23E-9",4:"1.234E-9",5:"1.2345E-9",6:"1.23456E-9"}
        deci_example_dict={1:"1.2",2:"1.23",3:"1.234",4:"1.2345",5:"1.23456",6:"1.234567"}
        if sigfig==True:
            if correct_ans_len>=5:
                correct_ans=sigfig2.scientific(correct_ans,n)
                n=n-1
                example=sig_example_dict[n]
                sci_not="Please input answer as scientific notation, like "+example+"."
            else:
                correct_ans=sigfig2.string(correct_ans,n)
                sci_not=""
        elif sigfig==False:
            if correct_ans_len>=5:
                correct_ans=Format.format_e(correct_ans,n)
                example=deci_example_dict[n]
                sci_not="Please input answer as scientific notation, like "+example+"."   #The variable sci_not will print and tell the user if they need to use sci notation
            else:
                n="%."+str(n)+"f"
                correct_ans=n%correct_ans    #Uses n that was declared earlier to format correct_ans as a string
                sci_not=""
        return correct_ans, sci_not
    def determine_sigfig(str_value):
        string_value=str(str_value)
        for d in string_value:
            if d==".":
                string_value=string_value.replace(".","")
                int_value=int(string_value)
                sig_numbers=len(str(int_value))
                return sig_numbers
            elif d==",":
                string_value=string_value.replace(",","")
                int_value=int(string_value)
                sig_numbers=len(str(int_value))
                return sig_numbers
        int_value=int(string_value)
        sig_numbers=len(str(int_value))
        return sig_numbers
    def roundup(final_vol):
        return int(math.ceil(final_vol/100.0))*100
    def format_answer(ans,export=False):
        plus=ans.find("+")
        if export==False:
            if plus>-1:
                no_plus=ans.replace("+","")
                no_space=no_plus.replace(" ","")  #This gets rid of the space between the value and the unit
                E_loc=no_space.find("E")
                beg=no_space[:E_loc]
                end=no_space[E_loc:]
                end=end.replace("0","")
                final=beg+end
                return final
            else:
                no_space=ans.replace(" ","")
                E_loc=no_space.find("E")
                beg=no_space[:E_loc]
                end=no_space[E_loc:]
                end=end.replace("0","")
                final=beg+end
                return final
        elif export==True:
            if plus>-1:
                no_plus=ans.replace("+","")
                E_loc=no_plus.find("E")
                beg=no_plus[:E_loc]
                end=no_plus[E_loc:]
                end=end.replace("0","")
                final=beg+end
                return final
            else:
                E_loc=ans.find("E")
                beg=ans[:E_loc]
                end=ans[E_loc:]
                end=end.replace("0","")
                final=beg+end
                return final
class Quest:
    """This contains methods that will help form and solve the question"""
    def unit_selection():
        unit_pool_simple=["Y","Z","E","P","T","G","M","k","h","da",
                            "d","c","m","u","n","p","f","a","z","y"]  #List of some SI metric units
        measure_pool=["m","L","g"]
        while True: #This loop will get random units and if the start==end units the loop will roll again until start!=end
            start_units=random.choice(unit_pool_simple)
            end_units=random.choice(unit_pool_simple)
            measure=random.choice(measure_pool)
            if start_units==end_units:
                continue
            else:
                break
        return start_units, end_units, measure
    def unit_selection_complex():
        #unit_pool_imperial=["density","molarity","atm","kPa","torr","Celsius","Kelvin","wavelength","frequency","pH","[H3O+]","Kw","temp","Kc","deltaG"]
        unit_pool_complex=["atm","kPa","torr"]
        while True:
            start_units=random.choice(unit_pool_complex)
            end_units=random.choice(unit_pool_complex)
            if start_units==end_units:
                continue
            else:
                break
        return start_units, end_units
    def how_to_solve(start_value,start_units,end_units):
        solve={"Y":24,"Z":21,"E":18,"P":15,"T":12,"G":9,"M":6,"k":3,"h":2,"da":1,
                "d":-1,"c":-2,"m":-3,"u":-6,"n":-9,"p":-12,"f":-15,"a":-18,"z":-21,"y":-24} #Stores the base10 values for each unit
        correct_ans=start_value*(10**(solve[start_units]-solve[end_units]))
        return correct_ans
    def how_to_solve_complex(start_value,start_units,end_units):
        key=start_units+"|"+end_units
        solve={"atm|kPa":101.325,"kPa|atm":0.00986923, "torr|atm":0.00131579,
                "atm|torr":760,"kPa|torr":7.50062,"torr|kPa":0.133322,
                "Celsius|Kelvin":273.15,"Kelvin|Celsius":-273.15}
        if start_units=="Celsius" or start_units=="Kelvin":
            correct_ans=start_value+solve[key]
        else:
            correct_ans=start_value*solve[key]
        return correct_ans
class PopUp:
    def __init__(self):
        self.window2=Toplevel() #Toplvel() is all you need, it needs to arguements
        self.window2.title("Export")
        self.window2.geometry("200x150") #widthxlength
        self.window2_instruct=Label(self.window2,text="Which question would you like to print, from 1-4?\n",wraplength=200,font="none 12 bold").grid(row=0,column=0,sticky=W)
        self.user_entry_ques_var=StringVar()    #This sets up to program to catch the input
        self.user_entry_ques=Entry(self.window2,width=10,bg="#76FB28",fg="black",textvariable=self.user_entry_ques_var)
        self.user_entry_ques.grid(row=2,column=0,sticky=W)
        self.window2_enter_button=Button(self.window2,text="Enter",width=5,bg="#FD74B2",command=self.export).grid(row=3,column=0,sticky=W)
    def export(self):
        text_export(self.user_entry_ques_var.get())
class MainWindow:
    def __init__(self, window): #__init__ is always ran
        self.window=window
        self.window.title("Unit Convert Practice")
        self.window.configure(background="#F2F6FA")
        #Banner
        self.photo1=PhotoImage(file="beakers.gif")
        self.banner=Label(window,image=self.photo1,bg="#F2F6FA").grid(row=0, column=0, sticky=N)
        self.question_title=Label(window,text="Question:\t\t(The textbox below is scrollable)",fg="black",font="none 12 bold").grid(row=8,column=0, sticky=W)
        #The place where the question will appear
        self.output_scroll=Scrollbar(window)
        self.output_scroll.grid(row=9,column=1,sticky=E)
        self.output=Text(window,width=85,height=4,wrap=WORD,background="#F2F6FA",yscrollcommand=self.output_scroll.set)
        self.output.grid(row=9,column=0,columnspan=2,sticky=W)
        self.output_scroll.config(command=self.output.yview)
        #Little title that says "Questions:" and buttons where the user can press to recieve a question
        self.instructions=Label(window,text="Please choose option:",fg="black",font="none 12 bold").grid(row=1,column=0,sticky=W) #bg=background colour of the text area, fg=text colour
        self.quest1_button=Button(window,text="Try Question 1)",bg="#39D7F8",width=15, command=self.output_Q1print).grid(row=2,column=0, sticky=W)
        self.quest2_button=Button(window,text="Try Question 2)",bg="#39D7F8",width=15, command=self.output_Q2print).grid(row=3,column=0, sticky=W)
        self.quest3_button=Button(window,text="Try Question 3)",bg="#39D7F8",width=15, command=self.output_Q3print).grid(row=4,column=0, sticky=W)
        self.quest4_button=Button(window,text="Try Question 4)",bg="#39D7F8",width=15, command=self.output_Q4print).grid(row=5,column=0, sticky=W)
        self.export_button=Button(window,text="Question Export",bg="#76FB28",width=15, command=PopUp).grid(row=6,column=0, sticky=W)
        self.about_button=Button(window,text="About",bg="#FD74B2",width=15, command=self.popup_credit).grid(row=7,column=0, sticky=W)
        #The place where the user will input their answer and hit a button to check if they are right or not
        self.user_entry=Entry(window, width=15, bg="#76FB28",fg="black")
        self.user_entry.grid(row=10, column=0, sticky=W)
        self.answer_button=Button(window,text="Enter",bg="#FD74B2",width=5, command=self.check).grid(row=11,column=0, sticky=W)
        self.exit_button=Button(window,text="Exit",bg="#FD74B2",width=5,command=self.quit).grid(row=11,column=0, sticky=E)
    def output_Q1print(self):
        question, self.answer=question1_print()
        self.output.delete(0.0, END)
        self.output.insert(END, question)
        print(Format.format_answer(self.answer))
    def output_Q2print(self):
        question, self.answer=question2_print()
        self.output.delete(0.0, END)
        self.output.insert(END, question)
        print(Format.format_answer(self.answer))
    def output_Q3print(self):
        question, self.answer=question3_print()
        self.output.delete(0.0, END)
        self.output.insert(END, question)
        print(Format.format_answer(self.answer))
    def output_Q4print(self):
        question, self.answer=question4_print()
        self.output.delete(0.0, END)
        self.output.insert(END, question)
        print(Format.format_answer(self.answer))
    def popup_credit(self):
        cred="Thanks to Alex Corrie, the creator of sigfig.py.\nThanks to Professor McBrayer, his tutelage allowed for the creation of Unit Convert"
        tkinter.messagebox.showinfo(title="About",message=cred)
    def check(self):
        format_correct_answer=Format.format_answer(self.answer)
        format_user_answer=Format.format_answer(self.user_entry.get())
        if format_correct_answer==format_user_answer:
            self.output.insert(END, "\nCorrect!")
        else:
            self.output.insert(END, "\nNot quite, please try again.")
    def quit(self):
        sys.exit()
#Question 1, just plain jane print
def question1():
    print("How many grams of NaCl are needed to make 200 mL of 3 g/L solution?")
    Final_Conc=3    #The variables of this question is kinda messy
    Final_Vol=200
    #ans=0.6 #NaCl
    correct_ans_units="g"
    correct_ans=(Final_Conc/1000)*Final_Vol
    print("answer key:",correct_ans)
    while True: #This is the answer value and unit loop, it will allow the user to come back to the beginning if they get it wrong along with the return on line 45
        while True: #This is the answer value loop
            try:
                ans=float(input("Please enter the final value: "))
            except ValueError:
                print("This input needs to be a number like 5.8, it doesn't take characters, please try again")
                continue
            else:
                break
        while True: #This is the answer unit loop
            try:
                ans_units=str(input("Please enter the final units: "))
            except ValueError:
                print("This input needs to be characters, not numbers, please try again")
                continue
            else:
                break
        if correct_ans==ans and correct_ans_units==ans_units: #Results of what the user puts in, right/wrong print
            print("Correct!")
            return
        elif correct_ans==ans and correct_ans_units!=ans_units:
            print("Your value is correct but double check your units")
        elif correct_ans!=ans and correct_ans_units==ans_units:
            print("Your units are right but double check your value")
    else:
        print("Your value and units are wong, please try again")
#Modified version of Question 1
def question1_print():
    #Phase 1: Setup
    final_conc=random.randint(1,8)
    final_vol=random.randint(100,500)
    final_vol=Format.roundup(final_vol)
    #Phase 2: Format
    correct_ans=(final_conc/1000)*final_vol
    final_vol=str(final_vol)
    final_conc=str(final_conc)
    correct_ans=round(correct_ans,2)
    correct_ans=str(correct_ans)
    #Phase 3: Final product
    question="How many grams of NaCl are needed to make "+final_vol+" mL of "+final_conc+" g/L solution? Round to 1 decimal places"
    correct_ans_units="g"
    answer_key=correct_ans+" "+correct_ans_units
    return question, answer_key
#Question 2, asks the user to solve an SI unit conversion question
def question2():
    n=random.randint(1,4) #This gives us a random decimal place, from 1-4, to round our start_value
    start_value=round(random.uniform(10,5000),n)  #Gives a random start value to work with and rounds to n decimal places
    start_units, end_units, measure=Quest.unit_selection() #Loads the variable start_units and end_units with a random set of SI units from the function
    correct_ans=Quest.how_to_solve(start_value,start_units,end_units) #Compares the start_units and end_units to solve the question and stores it in the variable correct_ans
    correct_ans_len=len(str(correct_ans))   #Reads the length of correct_ans and determines if the correct_ans needs to be formatted into sci notation or not
    correct_ans, sci=Format.sci_not(correct_ans,n)
    correct_ans_units=end_units+measure #Passes the end_units to correct_ans_units to later compare to the answer the user puts in
    print("What is",start_value,start_units+measure+" in",end_units+measure+"? "+"Round to the",n,"decimal place(s).",sci)  #Prints the question
    print("answer key:",correct_ans)    #This prints the answer so the programmer dooesn't need to calc the answer everytime, should be removed when the program goes live
    print("anser key:",correct_ans_units)
    while True: #This is the answer value and unit loop, it will allow the user to come back to the beginning if they get it wrong
        while True: #This is the answer value loop
            try:
                ans=str(input("Please enter the final value: "))
                float(ans)
            except ValueError:
                print("This input needs to be a number, it doesn't take characters, please try again")
                continue
            else:
                break
        while True: #This is the answer unit loop
            try:
                ans_units=str(input("Please enter the final units: "))
            except ValueError:
                print("This input needs to be characters, not numbers, please try again")
                continue
            else:
                break
        if correct_ans==ans and correct_ans_units==ans_units: #Results of what the user puts in, right/wrong print
            print("Correct!")
            return
        elif correct_ans==ans and correct_ans_units!=ans_units:
            print("Your value is correct but double check your units")
        elif correct_ans!=ans and correct_ans_units==ans_units:
            print("Your units are right but double check your value")
        else:
            print("Your value and units are wrong, please try again")
#Modified verison of Question 2
def question2_print():
    #Phase 1: Setup
    n=random.randint(1,4) #This gives us a random decimal place, from 1-4, to round our start_value
    start_value=round(random.uniform(10,5000),n)  #Gives a random start value to work with and rounds to n decimal places
    start_units, end_units, measure=Quest.unit_selection()  #Determines what the question is asking
    #Phase 2: Format
    correct_ans=Quest.how_to_solve(start_value,start_units,end_units) #Compares the start_units and end_units to solve the question and stores it in the variable correct_ans
    correct_ans, sci=Format.sci_not(correct_ans,n)  #Gets the answer and if the user needs to use scientific notation
    start_value=str(start_value)    #Makes start_value a string so that it can get printed in the question variable
    #Phase 3: Final product
    correct_ans_units=end_units+measure #Passes the end_units to correct_ans_units to later compare to the answer the user puts in
    n=str(n)    #Makes n a string so it can be joined later in the text_export() function
    question=("What is "+start_value+" "+start_units+measure+" in "+end_units+measure+"? "+"Round to "+n+" decimal place(s). "+sci)  #Prints the question
    answer_key=correct_ans+" "+correct_ans_units
    return question, answer_key
#Question 3, just like question 2 but asks the user for the sigfig
def question3():
    n=random.randint(1,2)
    start_value=round(random.uniform(10,5000),n)
    start_units, end_units, measure=Quest.unit_selection()
    sigfigs=len(str(start_value))
    sigfig_true=True
    correct_ans=Quest.how_to_solve(start_value,start_units,end_units)
    correct_ans, sci=Format.sci_not(correct_ans,sigfigs,sigfig_true)
    print("What is",start_value,start_units+measure+" in",end_units+measure+"? "+"Round to the nearest sigfig(s).",sci)
    print("answer key value:",correct_ans)
    correct_ans_units=end_units+measure
    print("answer key units:",correct_ans_units)
    while True:
        while True:
            try:
                ans=str(input("Please enter the final value: "))
                float(ans)
            except ValueError:
                print("This input needs to be a number, it doesn't take characters, please try again")
                continue
            else:
                break
        while True:
            try:
                ans_units=str(input("Please enter the final units: "))
            except ValueError:
                print("This input needs to be characters, not numbers, please try again")
                continue
            else:
                break
        if correct_ans==ans and correct_ans_units==ans_units:
            print("Correct!")
            return
        elif correct_ans==ans and correct_ans_units!=ans_units:
            print("Your value is correct but double check your units")
        elif correct_ans!=ans and correct_ans_units==ans_units:
            print("Your units are right but double check your value")
        else:
            print("Your value and units are wrong, please try again")
#Modified verison of Question 3
def question3_print():
    #Phase 1: Setup
    n=random.randint(1,2)   #n=decimal place
    start_value=round(random.uniform(1,1000),n)    #Rounds to the decimal place
    start_units, end_units, measure=Quest.unit_selection()  #Determines what the question is asking
    #Phase 2: Format
    correct_ans=Quest.how_to_solve(start_value, start_units, end_units)
    sigfig_boolean=True
    sigfigs=len(str(start_value))   #Since we're using SI units for this question the only number that determine sigfigs is start_value
    correct_ans, sci=Format.sci_not(correct_ans,sigfigs,sigfig_boolean)
    correct_ans_units=end_units+measure
    n=str(n)
    start_value=str(start_value)    #Making it a string so it can be concatenated in the question variable
    #Phase 3: Final product
    question=("What is "+start_value+" "+start_units+measure+" in "+end_units+measure+"? "+"Use correct sigfig(s). "+sci)  #Prints the question
    answer_key=correct_ans+" "+correct_ans_units
    return question, answer_key
#Question 4, this is a question with a complex/compound unit
def question4():
    n=random.randint(1,2)
    start_value=round(random.uniform(10,9000),n)
    start_units, end_units=Quest.unit_selection_complex()
    sigfig_value=Format.amount_sigfig(start_value,start_units,end_units)
    sigfig_true=True
    correct_ans=Quest.how_to_solve_complex(start_value,start_units,end_units)
    correct_ans, sci=Format.sci_not(correct_ans,sigfig_value,sigfig_true)
    print("What is",start_value,start_units,"in",end_units+"?","Round to the nearest sigfig(s).",sci)
    print("answer key value:",correct_ans)
    correct_ans_units=end_units
    print("answer key units:",correct_ans_units)
    while True:
        while True:
            try:
                ans=float(input("Please enter the final value: "))
            except ValueError:
                print("This input needs to be a number like 5.8 or 300, it doesn't take characters, please try again")
                continue
            else:
                break
        if correct_ans==ans:
            print("Correct!")
            return
        elif correct_ans!=ans:
            print("Your value is incorrect, please try again")
#Modified verison of Question 4
def question4_print():
    #Phase 1: Setup
    n=random.randint(1,2)   #Decimals
    start_value=round(random.uniform(10,9000),n)    #Random start_value
    start_units, end_units=Quest.unit_selection_complex()   #Determines what is asked
    #Phase 2: Format
    correct_ans=Quest.how_to_solve_complex(start_value,start_units,end_units)
    start_value=str(start_value)
    sigfig_boolean=True
    sigfig_value=Format.amount_sigfig(start_value,start_units,end_units)    #Finds sigfigs
    correct_ans, sci=Format.sci_not(correct_ans,sigfig_value,sigfig_boolean)
    n=str(n)
    #Phase 3: Final product
    question=("What is "+start_value+" "+start_units+" in "+end_units+"? "+" Use correct sigfig(s). "+sci)
    correct_ans_units=end_units
    answer_key=correct_ans+" "+correct_ans_units
    return question, answer_key
#Prints questions
def text_export(num):
    doc_ques=open("Practice Problems.txt","w")
    doc_ans=open("Answer key.txt","w")
    quest_select={"1":question1_print,"2":question2_print,"3":question3_print,"4":question4_print}
    """
    print("Which question would you like?")
    while True:
        try:
            choice=input()
        except:
            KeyError
            print("That is not a selection, please try again. Your options are 2,3")
        else:
            break
    print("How many questions would you like?")
    amount=int(input())
    """
    choice=num
    amount=10
    count=1
    for x in range(amount):
        question, answer=quest_select[choice]()
        question=str(question)
        answer=str(answer)
        format_boolean=True
        answer=Format.format_answer(answer,format_boolean)
        doc_ques.write(str(count))
        doc_ques.write(") ")
        doc_ques.write(question)
        doc_ques.write("\n")
        doc_ans.write(str(count))
        doc_ans.write(") ")
        doc_ans.write(answer)
        doc_ans.write("\n")
        count+=1
    doc_ques.close()
    doc_ans.close()
#This will just give a exit message when the user leaves the program
def bye_bye():
    farwell_dict={1:"Later gator!",2:"Have a great day!",3:"Bye bye!",4:"Farwell!",5:"Adios!",6:"Au revoir!",7:"Addio!",8:"Tchau!",9:"Pa!",10:"Vale!"}
    farwell_key=random.randint(1,10)
    farwell=farwell_dict[farwell_key]
    sys.exit(farwell)
#This will be like menu page where the user can pick their option
def main():
    while True:
        print("Note: Please make sure to include leading zero in your answer")
        print("Please choose an option")
        print("1) Try problem 1")
        print("2) Try problem 2")
        print("3) Try problem 3")
        print("4) Try problem 4")
        print("5) Export to text file")
        print("6) Credits")
        print("7) Exit")
        question_selection={"1":question1,"2":question2,"3":question3,"4":question4,"5":text_export,"6":credits,"7":bye_bye}
        while True:
            try:
                choice = input()
                question_selection[choice]()
            except KeyError:
                    print("That is not a selection, please try again")
            else:
                break
        print("\n")
        main()

#main() #This starts the program, for cmd

#GUI---------------------------------------------------

#Colors from beaker banner
#Green:  #76FB28
#Yellow:    #FDE512
#Blue:  #39D7F8
#Pink: #FD74B2
#White: #F2F6FA

#This starts the GUI
root=Tk()
GUI=MainWindow(root)
root.mainloop()
