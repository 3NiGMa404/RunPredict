from tkinter import *    #Import the tkinter library for GUI
import tkinter.font as font
from tkinter import ttk
import sklearn           #Import sklearn for linear regression
import sqlite3
import math

connection=sqlite3.connect('database.db')
cur=connection.cursor()
#cur.execute('''CREATE TABLE Runs(iD integer, Name text, Distance real, Time real, Conditions text, Temperature real, Humidity integer, Day text, HourOfDay integer, MinuteOfDay integer)''')
#cur.execute('''DELETE FROM Runs''' )
#connection.commit()
print([i for i in cur.execute('''SELECT * FROM Runs;''')])
print('\n\n\n')
window=Tk()
window.state('zoomed')         #Define the window attributes
window.title('RunPredict')
window.geometry("1920x1080")
window.configure(bg='#f0f0f0')
Button_Font = font.Font(family='Microsoft Sans Serif',size=15)
Label_Font = font.Font(family='Microsoft Sans Serif',size=15,weight="bold")         #Create fonts for buttons and labels
Add_Button_Photo = PhotoImage(file = "Add Button.PNG").subsample(2,2)
Predict_Button_Photo = PhotoImage(file = "Predict Button.PNG").subsample(2,2)          #Get images for buttons
Edit_Button_Photo = PhotoImage(file = "Edit Button.PNG").subsample(2,2)          #Get images for buttons

List_Box_Frame_1=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=1)
List_Box_Frame_2=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=1)
List_Box_Frame_3=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=1)
List_Box_Frame_4=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=1)

List_Box=Listbox(List_Box_Frame_1)                   #Create list box
List_Box_2=Listbox(List_Box_Frame_2)                   #Create list box
List_Box_3=Listbox(List_Box_Frame_3)
List_Box_4=Listbox(List_Box_Frame_4)

def Quantify_Data(data):
    Processed_Data=[]
    
    for record in data:
        processed_record=[]
        X=[0]*50
        if record[4]=="Heavy Rain": X[0]=1
        if record[4]=="Light Rain": X[1]=1
        if record[4]=="Sunny": X[2]=1
        if record[4]=="Overcast": X[3]=1
        if record[4]=="Fog": X[4]=1
        if record[4]=="Snow": X[5]=1
        
        if record[5]<5: X[6]=1
        if 5<=record[5]<10: X[7]=1
        if 10<=record[5]<15: X[8]=1
        if 15<=record[5]<20: X[9]=1
        if 20<=record[5]<25: X[10]=1
        if 25<=record[5]<30: X[11]=1
        if 30<=record[5]: X[12]=1

        if record[6]<20: X[13]=1
        if 20<=record[6]<40: X[14]=1
        if 40<=record[6]<60: X[15]=1
        if 60<=record[6]<80: X[16]=1
        if 80<=record[6]: X[17]=1

        if record[7]=="Monday": X[18]=1
        if record[7]=="Tuesday": X[19]=1
        if record[7]=="Wednesday": X[20]=1
        if record[7]=="Thursday": X[21]=1
        if record[7]=="Friday": X[22]=1
        if record[7]=="Saturday": X[23]=1
        if record[7]=="Sunday": X[24]=1

        for i in range(0,24):
            if record[8]==i:
                X[26+i]=1
        processed_record.append(X)
        processed_record.append([record[3]])
            
        Processed_Data.append(processed_record)
    return Processed_Data

def UnQuantify_Data(data):
    Qualified_Data=[]
    for record in data:
        X=[]
        if record[0][0]==1: X.append("Heavy Rain")
        if record[0][1]==1: X.append("Light Rain")
        if record[0][2]==1: X.append("Sunny")
        if record[0][3]==1: X.append("Overcast")
        if record[0][4]==1: X.append("Fog")
        if record[0][5]==1: X.append("Snow")
        
        if record[0][6]==1: X.append(0)
        if record[0][7]==1: X.append(7.5)
        if record[0][8]==1: X.append(12.5)
        if record[0][9]==1: X.append(17.5)
        if record[0][10]==1: X.append(22.5)
        if record[0][11]==1: X.append(27.5)
        if record[0][12]==1: X.append(35)

        if record[0][13]==1: X.append(10)
        if record[0][14]==1: X.append(30)
        if record[0][15]==1: X.append(50)
        if record[0][16]==1: X.append(70)
        if record[0][17]==1: X.append(90)

        if record[0][18]==1: X.append("Monday")
        if record[0][19]==1: X.append("Tuesday")
        if record[0][20]==1: X.append("Wednesday")
        if record[0][21]==1: X.append("Thursday")
        if record[0][22]==1: X.append("Friday")
        if record[0][23]==1: X.append("Saturday")
        if record[0][24]==1: X.append("Sunday")
        for i in range(25,50):
            if record[0][i]==1:
                X.append('{}:00'.format(str(i - 25).zfill(2)))
        Qualified_Data.append(X)
    return Qualified_Data
                    
    

Quant=Quantify_Data([i for i in cur.execute('''SELECT * FROM Runs;''')])
print(Quant)
Qual=UnQuantify_Data(Quant)
print(Qual)
def Update_Listbox():
    counter=0
    List_Box.delete(0,END)
    List_Box_2.delete(0,END)
    List_Box_3.delete(0,END)
    List_Box_4.delete(0,END)
    for item in cur.execute('''SELECT * FROM Runs;'''):  
        List_Box.insert(counter,str(item[0]))
        List_Box_2.insert(counter,str(item[1]))
        List_Box_3.insert(counter,str(item[2])+"km")
        List_Box_4.insert(counter,str(math.floor(item[3]/60))+":"+str(int(round(item[3]%60))).zfill(2))
        counter+=1
Update_Listbox()
def Onselect(event):
    selected=List_Box_2.curselection()
    if len(selected)==0:
        selected=List_Box_3.curselection()
    if len(selected)==0:
        selected=List_Box_4.curselection()
    if len(selected)>0:
        List_Box.select_set(selected)
    
List_Box_2.bind("<<ListboxSelect>>",Onselect)
List_Box_3.bind("<<ListboxSelect>>",Onselect)
List_Box_4.bind("<<ListboxSelect>>",Onselect)

    
def Create_Predict_Window():
    Conditions_Clicked = StringVar()
    Day_Clicked = StringVar()
    Temperature_Var=StringVar(value=0)
    Humidity_Var=StringVar(value=0)                        #Instantiate variables for conditions
    Hour_Var=StringVar(value=0)
    Minute_Var=StringVar(value=0)
    Distance_Var=StringVar(value=0)
    
    Predict_Window=Toplevel(window)
    Predict_Window.title("Predict Time")
    Predict_Window.geometry("400x500")                #Create window and window attributes
    Predict_Window.grab_set()
    
    Predict_Weather_Label=Label(Predict_Window, text="Weather",font=Label_Font,bd=0)
    Predict_Conditions_Label=Label(Predict_Window, text="Conditions: ",font=Button_Font,bd=0)
    Predict_Temperature_Label=Label(Predict_Window, text="Temperature (°C): ",font=Button_Font,bd=0)                     #Define labels
    Predict_Humidity_Label=Label(Predict_Window, text="Humidity (%): ",font=Button_Font,bd=0)
    Predict_Day_Label=Label(Predict_Window, text="Day and Time",font=Label_Font,bd=0)
    Predict_Week_Label=Label(Predict_Window, text="Day of Week: ",font=Button_Font,bd=0)
    Predict_Time_Label=Label(Predict_Window, text="Time of Day: ",font=Button_Font,bd=0)
    Predict_Predict_Label=Label(Predict_Window, text="Run",font=Label_Font,bd=0)
    Predict_Distance_Label=Label(Predict_Window, text="Distance: ",font=Button_Font,bd=0)
    Predict_Colon_Label=Label(Predict_Window,text=':',font=Button_Font)
    
    Predict_Conditions_Drop=OptionMenu(Predict_Window,Conditions_Clicked,"Sunny","Heavy Rain","Light Rain","Fog","Overcast","Snow")   #Define inputs
    Predict_Day_Drop=OptionMenu(Predict_Window,Day_Clicked,"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    Predict_Temperature_Input=Spinbox(Predict_Window,textvariable=Temperature_Var,from_=0,to=60)
    Predict_Humidity_Input=Spinbox(Predict_Window,textvariable=Humidity_Var,from_=0,to=100)
    Predict_Hour_Input=Spinbox(Predict_Window,textvariable=Hour_Var,from_=0,to=23,width=4,format='%02.0f')
    Predict_Minute_Input=Spinbox(Predict_Window,textvariable=Minute_Var,from_=0,to=59,width=4,format='%02.0f')
    Predict_Distance_Input=Spinbox(Predict_Window,textvariable=Distance_Var,from_=0,to=100,width=10,format='%3.2f',increment=0.01)
    Predict_Add_Button=Button(Predict_Window,image=Predict_Button_Photo,bg='#f0f0f0',relief=FLAT,width=150,height=54,bd=0)
    
    Predict_Weather_Label.place(x=0,y=0)
    Predict_Conditions_Label.place(x=10,y=40)
    Predict_Temperature_Label.place(x=10,y=80)
    Predict_Humidity_Label.place(x=10,y=120)
    Predict_Day_Label.place(x=0,y=160)
    Predict_Week_Label.place(x=10,y=200)
    Predict_Time_Label.place(x=10,y=240)
    Predict_Predict_Label.place(x=0,y=280)
    Predict_Distance_Label.place(x=10,y=320)           #Place labels and inputs
    Predict_Day_Drop.place(x=200,y=200)
    Predict_Conditions_Drop.place(x=200,y=40)
    Predict_Temperature_Input.place(x=200,y=80)
    Predict_Humidity_Input.place(x=200,y=120)
    Predict_Hour_Input.place(x=200,y=240)
    Predict_Minute_Input.place(x=250,y=240)
    Predict_Colon_Label.place(x=235,y=230)
    Predict_Distance_Input.place(x=200,y=320)
    Predict_Add_Button.place(x=240,y=430)
def delete():
    List_Box_2.curselection()
    cur.execute('DELETE FROM Runs WHERE iD = '+str(List_Box.get(List_Box.curselection())))
    connection.commit()
    Update_Listbox()
def Create_Run_Window(add):
    if add:
        Conditions_Clicked = StringVar()
        Day_Clicked = StringVar()
        Temperature_Var=StringVar(value=0)        #Instantiate variables
        Humidity_Var=StringVar(value=0)
        Hour_Var=StringVar(value=0)
        Minute_Var=StringVar(value=0)
        Distance_Var=StringVar(value=0)
        Time_Minute_Var=StringVar(value=0)
        Time_Second_Var=StringVar(value=0)
        Run_Name=StringVar()
    else:
        Record=[i for i in cur.execute('''SELECT * FROM Runs;''')][0]
        Conditions_Clicked = StringVar(value=Record[4])
        Day_Clicked = StringVar(value=Record[7])
        Temperature_Var=StringVar(value=Record[5])        #Instantiate variables
        Humidity_Var=StringVar(value=Record[6])
        Hour_Var=StringVar(value=Record[8])
        Minute_Var=StringVar(value=Record[9])
        Distance_Var=StringVar(value=Record[2])
        Time_Minute_Var=StringVar(value=Record[3]%60)
        Time_Second_Var=StringVar(value=math.floor(Record[3]/60))
        Run_Name=StringVar(value=Record[1])
    def Add():
        try:
            New_iD = [i for i in cur.execute('''SELECT MAX(iD) FROM Runs;''')][0][0]+1
        except:
            New_iD = 0
        True_Time=int(Time_Minute_Var.get())*60 + int(Time_Second_Var.get())
        cur.execute('INSERT INTO Runs VALUES ({},"{}",{},{},"{}",{},{},"{}",{},{});'.format(New_iD, Run_Name.get(),Distance_Var.get(),True_Time,Conditions_Clicked.get(),Temperature_Var.get(),Humidity_Var.get(),Day_Clicked.get(),Hour_Var.get(),Minute_Var.get()))
        connection.commit()
        Update_Listbox()

#iD integer, Name text, Distance real, Time real, Conditions text, Temperature real, Humidity integer, Day text, HourOfDay integer, MinuteOfDay integer
    def Edit():
        try:
            New_iD = [i for i in cur.execute('''SELECT MAX(iD) FROM Runs;''')][0][0]+1
        except:
            New_iD = 0
        True_Time=int(Time_Minute_Var.get())*60 + int(Time_Second_Var.get())
        cur.execute('UPDATE Runs SET Name="{}",Distance={},Time={},Conditions="{}",Temperature={},Humidity={},Day="{}",HourOfDay={},MinuteOfDay={} WHERE iD={};'.format(Run_Name.get(),Distance_Var.get(),True_Time,Conditions_Clicked.get(),Temperature_Var.get(),Humidity_Var.get(),Day_Clicked.get(),Hour_Var.get(),Minute_Var.get(),New_iD))
        connection.commit()
        Update_Listbox()
        
    Run_Window=Toplevel(window)
    Run_Window.title("Edit/Add Run")        #Create the run adding window and attributes
    Run_Window.geometry("400x500")
    Run_Window.grab_set()
    
    Run_Weather_Label=Label(Run_Window, text="Weather",font=Label_Font,bd=0)
    Run_Conditions_Label=Label(Run_Window, text="Conditions: ",font=Button_Font,bd=0)
    Run_Temperature_Label=Label(Run_Window, text="Temperature (°C): ",font=Button_Font,bd=0)
    Run_Humidity_Label=Label(Run_Window, text="Humidity (%): ",font=Button_Font,bd=0)
    Run_Day_Label=Label(Run_Window, text="Day and Time",font=Label_Font,bd=0)
    Run_Week_Label=Label(Run_Window, text="Day of Week: ",font=Button_Font,bd=0)           #Create labels
    Run_Time_Label=Label(Run_Window, text="Time of Day: ",font=Button_Font,bd=0)
    Run_Run_Label=Label(Run_Window, text="Run",font=Label_Font,bd=0)
    Run_Distance_Label=Label(Run_Window, text="Distance: ",font=Button_Font,bd=0)
    Run_Run_Time_Label=Label(Run_Window, text="Time: ",font=Button_Font,bd=0)
    Run_Colon_Label=Label(Run_Window,text=':',font=Button_Font)
    Run_Name_Label = Label(Run_Window,text="Run Name: ", font=Button_Font,bd=0)
    
    Run_Conditions_Drop=OptionMenu(Run_Window,Conditions_Clicked,"Sunny","Heavy Rain","Light Rain","Fog","Overcast","Snow")
    Run_Day_Drop=OptionMenu(Run_Window,Day_Clicked,"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    Run_Temperature_Input=Spinbox(Run_Window,textvariable=Temperature_Var,from_=0,to=60)
    Run_Humidity_Input=Spinbox(Run_Window,textvariable=Humidity_Var,from_=0,to=100)
    Run_Hour_Input=Spinbox(Run_Window,textvariable=Hour_Var,from_=0,to=23,width=4,format='%02.0f')         #Create inputs
    Run_Minute_Input=Spinbox(Run_Window,textvariable=Minute_Var,from_=0,to=59,width=4,format='%02.0f')
    Run_Distance_Input=Spinbox(Run_Window,textvariable=Distance_Var,from_=0,to=100,width=10,format='%3.2f',increment=0.01)
    Run_Time_Min_Input=Spinbox(Run_Window,textvariable=Time_Minute_Var,from_=0,to=500,width=4,format='%02.0f')
    Run_Time_Second_Input=Spinbox(Run_Window,textvariable=Time_Second_Var,from_=0,to=59,width=4,format='%02.0f')
    Run_Colon_Label_2=Label(Run_Window,text=':',font=Button_Font)
    if add:
        Run_Add_Button=Button(Run_Window,image=Add_Button_Photo,bg='#f0f0f0',relief=FLAT,width=150,height=54,bd=0,command=Add)
    else:
        Run_Add_Button=Button(Run_Window,image=Edit_Button_Photo,bg='#f0f0f0',relief=FLAT,width=150,height=54,bd=0,command=Edit)
    Run_Name_Field=Entry(Run_Window,textvariable=Run_Name)

    
    Run_Weather_Label.place(x=0,y=0)
    Run_Conditions_Label.place(x=10,y=40)
    Run_Temperature_Label.place(x=10,y=80)
    Run_Humidity_Label.place(x=10,y=120)
    Run_Day_Label.place(x=0,y=160)
    Run_Week_Label.place(x=10,y=200)
    Run_Time_Label.place(x=10,y=240)
    Run_Run_Label.place(x=0,y=280)
    Run_Distance_Label.place(x=10,y=320)
    Run_Run_Time_Label.place(x=10,y=360)
    Run_Day_Drop.place(x=200,y=200)
    Run_Conditions_Drop.place(x=200,y=40)           #Place inputs and labels
    Run_Temperature_Input.place(x=200,y=80)
    Run_Humidity_Input.place(x=200,y=120)
    Run_Hour_Input.place(x=200,y=240)
    Run_Minute_Input.place(x=250,y=240)
    Run_Colon_Label.place(x=235,y=230)
    Run_Distance_Input.place(x=200,y=320)
    Run_Time_Min_Input.place(x=200,y=360)
    Run_Time_Second_Input.place(x=250,y=360)
    Run_Colon_Label_2.place(x=235,y=350)
    Run_Name_Label.place(x=0,y=400)
    Run_Name_Field.place(x=200,y=405)

    Run_Add_Button.place(x=240,y=430)
def add_window():
    Create_Run_Window(True)
def edit_window():
    Create_Run_Window(False)
def Create_Ideal_Window():
    Distance_Var=StringVar(value=0)            #Create distance variable
    
    Ideal_Window=Toplevel(window)
    Ideal_Window.title("Predict Ideal Conditions")
    Ideal_Window.geometry("400x500")                   #Create window with attributes
    Ideal_Window.grab_set()
    
    Ideal_Distance_Label=Label(Ideal_Window, text="Run Distance ",font=Label_Font,bd=0)
    Ideal_Distance_Label_2=Label(Ideal_Window, text="Distance: ",font=Button_Font,bd=0)      #Create Labels
    
    Ideal_Distance_Input=Spinbox(Ideal_Window,textvariable=Distance_Var,from_=0,to=100,width=10,format='%3.2f',increment=0.01)
    Ideal_Predict_Button=Button(Ideal_Window,image=Predict_Button_Photo,bg='#f0f0f0',relief=FLAT,width=150,height=54,bd=0)    #Create button and input
    
    Ideal_Distance_Label.place(x=0,y=10)
    Ideal_Distance_Label_2.place(x=10,y=50)
    Ideal_Distance_Input.place(x=200,y=50)               #Place labels
    Ideal_Predict_Button.place(x=240,y=430)


Scrollbox=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=10,height=1000)

scrollbar = Scrollbar(Scrollbox,orient=VERTICAL)
Time_Button_Border = Frame(window, highlightbackground = "black", highlightthickness = 2, bd=0)                  #Create a border for the time predict button and the button itself
Time_Button=Button(Time_Button_Border,text="Predict Time From Conditions",font=Button_Font,bg='#edead9',relief=FLAT,bd=10,width=22,command=Create_Predict_Window)

Ideal_Button_Border = Frame(window, highlightbackground = "black", highlightthickness = 2, bd=0)                  #Create a border for the conditions predict button and the button itself
Ideal_Button=Button(Ideal_Button_Border,text="Predict Ideal Conditions",font=Button_Font,bg='#edead9',relief=FLAT,bd=10,width=22,command=Create_Ideal_Window)

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


Edit_Button=Button(Edit_Button_Border,text="Edit",font=Button_Font,bg='#b5d9fe',relief=FLAT,bd=5,width=7,command=edit_window)
Add_Button=Button(Add_Button_Border,text="Add",font=Button_Font,bg='#b5d9fe',relief=FLAT,bd=5,width=7,command=add_window)         #Create Edit, Add and Delete buttons                        #Create the edit, add and delete buttons
Delete_Button=Button(Delete_Button_Border,text="Delete",font=Button_Font,bg='#f9c7c7',relief=FLAT,bd=5,width=7,command=delete)



Edit_Button_Border.grid(row=0,column=0)
Add_Button_Border.grid(row=0,column=1)
Delete_Button_Border.grid(row=0,column=2)
Blank_Box=Label(Scrollbox,height=10,width=1)
Scrollbox.place(x=1150,y=100)
Blank_Box.grid(row=0,column=1)

scrollbar.grid(row=0,column=0,sticky=NS)
List_Box.config(yscrollcommand = scrollbar.set)
List_Box_2.config(yscrollcommand = scrollbar.set)
List_Box_3.config(yscrollcommand = scrollbar.set)
List_Box_4.config(yscrollcommand = scrollbar.set)
def multiple_yview(*args):
    List_Box.yview(*args)
    List_Box_2.yview(*args)
    List_Box_3.yview(*args)
    List_Box_4.yview(*args)
    
scrollbar.config(command = multiple_yview)
List_Box_Frame_1.place(x=800,y=100)
List_Box_Frame_2.place(x=850,y=100)
List_Box_Frame_3.place(x=950,y=100)
List_Box_Frame_4.place(x=1050,y=100)
List_Box.pack()
List_Box_2.pack()
List_Box_3.pack()
List_Box_4.pack()

Edit_Add_Delete_Border.place(x=800,y=400)
Weather_Label.place(x=200,y=165)
Day_Time_Label.place(x=200,y=195)                           #Place everything
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
