from tkinter import *    #Import the tkinter library for GUI
import tkinter.font as font
from tkinter import ttk
import sklearn           #Import sklearn for linear regression
#import 


window=Tk()
window.state('zoomed')         #Define the window attributes
window.title('RunPredict')
window.geometry("1920x1080")
window.configure(bg='#f0f0f0')

Button_Font = font.Font(family='Microsoft Sans Serif',size=15)
Label_Font = font.Font(family='Microsoft Sans Serif',size=15,weight="bold")


Time_Button_Border = Frame(window, highlightbackground = "black", highlightthickness = 2, bd=0)                  #Create a border for the time predict button and the button itself
Time_Button=Button(Time_Button_Border,text="Predict Time From Conditions",font=Button_Font,bg='#edead9',relief=FLAT,bd=10,width=22)

Ideal_Button_Border = Frame(window, highlightbackground = "black", highlightthickness = 2, bd=0)                  #Create a border for the conditions predict button and the button itself
Ideal_Button=Button(Ideal_Button_Border,text="Predict Ideal Conditions",font=Button_Font,bg='#edead9',relief=FLAT,bd=10,width=22)

Weather_Var = StringVar()
Weather_Label = Label(window, textvariable=Weather_Var,font=Label_Font,bd=0)            #Weather label text variable and data
Weather_Var.set("Weather: ")

Day_Time_Var = StringVar()
Day_Time_Label = Label(window, textvariable=Day_Time_Var,font=Label_Font,bd=0)            #Day and time label text variable and data
Day_Time_Var.set("Day and Time: ")

Distance_Var = StringVar()
Distance_Label = Label(window, textvariable=Distance_Var,font=Label_Font,bd=0)            #Distance label text variable and data
Distance_Var.set("Distance: ")

Time_Var = StringVar()
Time_Label = Label(window, textvariable=Time_Var,font=Label_Font,bd=0)            #Predicted time label text variable and data
Time_Var.set("Predicted Time: ")


Ideal_Condition_Var = StringVar()
Ideal_Condition_Label = Label(window, textvariable=Ideal_Condition_Var,font=Label_Font,bd=0)            #Weather label text variable and data
Ideal_Condition_Var.set("Ideal Conditions")

Weather_Ideal_Var = StringVar()
Weather_Ideal_Label = Label(window, textvariable=Weather_Ideal_Var,font=Label_Font,bd=0)            #Day and time label text variable and data
Weather_Ideal_Var.set("Weather: ")



Day_Time_Ideal_Var = StringVar()
Day_Time_Ideal_Label = Label(window, textvariable=Day_Time_Ideal_Var,font=Label_Font,bd=0)            #Predicted time label text variable and data
Day_Time_Ideal_Var.set("Day and Time: ")


Edit_Add_Delete_Border = Frame(window, highlightbackground = "black", highlightthickness = 1, bd=0)                              #Create a border to surround all the edit, add and delete buttons

Edit_Button_Border = Frame(Edit_Add_Delete_Border, highlightbackground = "black", highlightthickness = 1, bd=0)                  #Create a border for each edit, add and delete button
Add_Button_Border = Frame(Edit_Add_Delete_Border, highlightbackground = "black", highlightthickness = 1, bd=0)
Delete_Button_Border = Frame(Edit_Add_Delete_Border, highlightbackground = "black", highlightthickness = 1, bd=0) 


Edit_Button=Button(Edit_Button_Border,text="Edit",font=Button_Font,bg='#b5d9fe',relief=FLAT,bd=5,width=7)
Add_Button=Button(Add_Button_Border,text="Add",font=Button_Font,bg='#b5d9fe',relief=FLAT,bd=5,width=7)                              #Create the edit, add and delete buttons
Delete_Button=Button(Delete_Button_Border,text="Delete",font=Button_Font,bg='#f9c7c7',relief=FLAT,bd=5,width=7)

List_Box=Listbox(window)

Edit_Button_Border.grid(row=0,column=0)
Add_Button_Border.grid(row=0,column=1)
Delete_Button_Border.grid(row=0,column=2)
List_Box.place(x=800,y=100)
Edit_Add_Delete_Border.place(x=800,y=400)
Weather_Label.place(x=200,y=165)
Day_Time_Label.place(x=200,y=195)
Distance_Label.place(x=200,y=225)
Time_Label.place(x=200,y=255)
Ideal_Condition_Label.place(x=200,y=365)
Weather_Ideal_Label.place(x=200,y=395)
Day_Time_Ideal_Label.place(x=200,y=425)
Ideal_Button_Border.place(x=200,y=300)
Delete_Button.grid(row=0,column=2)
Time_Button_Border.place(x=200,y=100)
Ideal_Button.pack()
Edit_Button.pack()
Add_Button.pack()
Time_Button.pack()
window.mainloop()

#Existence check, Type Check, Range Check, Limited Choices
