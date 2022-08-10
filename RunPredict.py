from tkinter import *    #Import the tkinter library for GUI
import tkinter.font as font
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
from tkinter import ttk
from sklearn import linear_model         #Import sklearn for linear regression
import sqlite3
import math
import numpy as np
import os
import easygui


def Choose_File():                   #Create function to choose a .db file using the easygui fileopenbox function
    file=''
    while not file[-3:].lower()==".db":
        file=easygui.fileopenbox(filetypes=('Db files',"*.db"))
        if not file[-3:].lower()==".db":
            messagebox.showwarning(title="File Warning", message="Please choose a .db file, exiting...")   #Exit if they don't choose a .db file
            exit()
        return file

connection=sqlite3.connect(Choose_File())   #Connect to chosen .db file

cur=connection.cursor()

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
List_Box_Frame_3=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=1)      #Create frames for the various listboxes
List_Box_Frame_4=Frame(window, highlightbackground = "black", highlightthickness = 0, bd=0,width=1)


List_Box=Listbox(List_Box_Frame_1)                   #Create list box
List_Box_2=Listbox(List_Box_Frame_2)                   #Create list box
List_Box_3=Listbox(List_Box_Frame_3)
List_Box_4=Listbox(List_Box_Frame_4)

Weather_Var = StringVar()
Weather_Label = Label(window, textvariable=Weather_Var,font=Label_Font,bd=0)            #Weather label text variable and data
Weather_Var.set("Weather: ")

def Quantify_Data(data):                     #Create function to turn data from description into numbers
    Processed_Data=[]
    
    for record in data:
        processed_record=[]
        X=[0]*50
        if record[4]=="Heavy Rain": X[0]=1
        if record[4]=="Light Rain": X[1]=1    #Convert weather to numbers where a zero means it is not those conditions and a one means it is
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
        
        rounded_hour=(record[8] if record[9]<30 else record[8] + 1)
        for i in range(0,24):
            if rounded_hour==i:
                X[25+i]=1                                #Split the day into 24 hours, where a 1 represents the hour that the run was taken in and the rest are zeroes
        processed_record.append(X)
        processed_record.append([record[3]])
            
        Processed_Data.append(processed_record)
    return Processed_Data

def UnQuantify_Data(data):    #Create a function to turn numerical data back into words
    Qualified_Data=[]
    for record in data:
        X=[]
        if record[0][0]==1: X.append("Heavy Rain")
        if record[0][1]==1: X.append("Light Rain")
        if record[0][2]==1: X.append("Sunny")     #Turn the zeroes and ones back into weather
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
        if record[0][20]==1: X.append("Wednesday")     #Turn the zeroes and ones back into the days of the week
        if record[0][21]==1: X.append("Thursday")
        if record[0][22]==1: X.append("Friday")
        if record[0][23]==1: X.append("Saturday")
        if record[0][24]==1: X.append("Sunday")
        for i in range(25,50):
            if record[0][i]==1:
                X.append('{}:00'.format(str(i - 25).zfill(2)))
        Qualified_Data.append(X)
    return Qualified_Data                          #Return a list containing the day, weather and time
                    
    



def Update_Listbox():      #Update the listbox with the new runs when a run is added, edited or deleted
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
def Onselect(event):                     #Run function when an item from a listbox is selected
    selected=List_Box_2.curselection()
    if len(selected)==0:                     #When an item from a listbox is selected, change the first listbox to that selection
        selected=List_Box_3.curselection()
    if len(selected)==0:
        selected=List_Box_4.curselection()
    if len(selected)>0:
        List_Box.select_set(selected)
    
List_Box_2.bind("<<ListboxSelect>>",Onselect)
List_Box_3.bind("<<ListboxSelect>>",Onselect)               #Bind the listboxes to the onselect function
List_Box_4.bind("<<ListboxSelect>>",Onselect)

    
def Create_Predict_Window():
    Conditions_Clicked = StringVar()
    Day_Clicked = StringVar()
    Temperature_Var=StringVar(value=0)
    Humidity_Var=StringVar(value=0)                        #Instantiate variables for conditions
    Hour_Var=StringVar(value=0)
    Minute_Var=StringVar(value=0)
    Distance_Var=StringVar(value=0)
    def Predict_Time():
        Data_Raw=cur.execute('''SELECT * FROM Runs WHERE distance BETWEEN {} AND {};'''.format(float(Distance_Var.get())-0.01,float(Distance_Var.get())+0.01))
        Data=Quantify_Data(Data_Raw)             #Execute SQL and turn the data into 1s and 0s for regression
        X=[]
        Y=[]
        for i in Data:
            X.append(i[0])                            #Add the data to a X and Y  variables
            Y.append(i[1])
        Regression=linear_model.LinearRegression().fit(X,Y)         #Fit the regression to X and Y variables
        True_Time=int(Hour_Var.get())*60+int(Minute_Var.get())     #Get the time in seconds

        Quantified_Data=Quantify_Data([[0, ' ',float(Distance_Var.get()),True_Time,Conditions_Clicked.get(),float(Temperature_Var.get()),int(Humidity_Var.get()),Day_Clicked.get(),int(Hour_Var.get()),int(Minute_Var.get())]])
                                                                                                       #Turn the data for this specific run into 1s and 0s
        Weather_Var.set("Weather: {}, {}°C, {}% Humidity".format(Conditions_Clicked.get(),Temperature_Var.get(),Humidity_Var.get()))
        Prediction=Regression.predict([Quantified_Data[0][0]])[0][0]                                  #Get the predicted time for this specific run
        Time_Var.set("Predicted Time: {}:{}".format(math.floor(Prediction/60),str(int(Prediction%60)).zfill(2)))
        Day_Time_Var.set("Day and Time: "+ Day_Clicked.get() + " at " + Hour_Var.get() + ":" + Minute_Var.get())   #Update labels and destroy window
        Distance_Var_2.set("Distance: "+str(round(float(Distance_Var.get()),2))+"km")
        Predict_Window.destroy()
        
    
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
    Predict_Predict_Button=Button(Predict_Window,image=Predict_Button_Photo,bg='#f0f0f0',relief=FLAT,width=150,height=54,bd=0,command=Predict_Time)
    
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
    Predict_Predict_Button.place(x=240,y=430)
def delete():
    List_Box_2.curselection()
    cur.execute('DELETE FROM Runs WHERE iD = '+str(List_Box.get(List_Box.curselection())))   #Function to delete runs
    connection.commit()
    Update_Listbox()
def Create_Run_Window(add):
    if add:
        Conditions_Clicked = StringVar()
        Day_Clicked = StringVar()
        Temperature_Var=StringVar(value=0)        #Instantiate variables if window is in add mode
        Humidity_Var=StringVar(value=0)
        Hour_Var=StringVar(value=0)
        Minute_Var=StringVar(value=0)
        Distance_Var=StringVar(value=0)
        Time_Minute_Var=StringVar(value=0)
        Time_Second_Var=StringVar(value=0)
        Run_Name=StringVar()
    else:
        Record=[i for i in cur.execute('''SELECT * FROM Runs;''')][List_Box.curselection()[0]]
        Conditions_Clicked = StringVar(value=Record[4])
        Day_Clicked = StringVar(value=Record[7])
        Temperature_Var=StringVar(value=Record[5])        #Instantiate variables if window is in edit mode
        Humidity_Var=StringVar(value=Record[6])
        Hour_Var=StringVar(value=Record[8])
        Minute_Var=StringVar(value=Record[9])
        Distance_Var=StringVar(value=Record[2])
        Time_Minute_Var=StringVar(value=math.floor(Record[3]/60))
        Time_Second_Var=StringVar(value=Record[3]%60)
        Run_Name=StringVar(value=Record[1])
    def Add():
        try:
            New_iD = [i for i in cur.execute('''SELECT MAX(iD) FROM Runs;''')][0][0]+1     #Get new ID
        except:
            New_iD = 0
        True_Time=int(Time_Minute_Var.get())*60 + int(Time_Second_Var.get())
        cur.execute('INSERT INTO Runs VALUES ({},"{}",{},{},"{}",{},{},"{}",{},{});'.format(New_iD, Run_Name.get(),Distance_Var.get(),True_Time,Conditions_Clicked.get(),Temperature_Var.get(),Humidity_Var.get(),Day_Clicked.get(),Hour_Var.get(),Minute_Var.get()))
        connection.commit()                                                    #Add run to SQL
        Update_Listbox()

    def Edit():
        try:
            New_iD = [i for i in cur.execute('''SELECT MAX(iD) FROM Runs;''')][0][0]+1    #Get new ID
        except:
            New_iD = 0
        True_Time=int(Time_Minute_Var.get())*60 + int(Time_Second_Var.get())
        cur.execute('UPDATE Runs SET Name="{}",Distance={},Time={},Conditions="{}",Temperature={},Humidity={},Day="{}",HourOfDay={},MinuteOfDay={} WHERE iD={};'.format(Run_Name.get(),Distance_Var.get(),True_Time,Conditions_Clicked.get(),Temperature_Var.get(),Humidity_Var.get(),Day_Clicked.get(),Hour_Var.get(),Minute_Var.get(),New_iD))
        connection.commit()                    #Update SQL run
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
    Run_Week_Label=Label(Run_Window, text="Day of Week: ",font=Button_Font,bd=0)           #Create labels for the 
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
    Create_Run_Window(True)              #Create run and edit windows with predefined function
def edit_window():
    Create_Run_Window(False)
def Create_Ideal_Window():
    Distance_Var=StringVar(value=0)            #Create distance variable
    def Predict_Ideal():
        weather_types=["Heavy Rain","Light Rain","Sunny","Overcast","Fog","Snow"]
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        Data_Raw=cur.execute('''SELECT * FROM Runs WHERE distance BETWEEN {} AND {};'''.format(float(Distance_Var.get())-0.01,float(Distance_Var.get())+0.01))
        Data=Quantify_Data(Data_Raw)             #Turn data into 1s and 0s
        X=[]
        Y=[]
        for i in Data:
            X.append(i[0])
            Y.append(i[1])
        Regression=linear_model.LinearRegression().fit(X,Y)    #Fit regression to X and Y variables

        Coef=list(Regression.coef_[0])                   #Get the list of coefficients    

        Weather_Coef=Coef[0:5]
        
        for i in range(len(Weather_Coef)):                   # For each set of coefficients (weather, temperature, humidity, time of day and day of week,
            if Weather_Coef[i] == 0:                         # find the minimum coefficient (that is the one that lowers the predicted time by the most)
                Weather_Coef[i] = 100                        # and create an "ideal" variable with the data point attributed to that coefficient
        Ideal_Weather=weather_types[Weather_Coef.index(min(Weather_Coef))]
        
        Temperature_Coef=Coef[6:12]
        for i in range(len(Temperature_Coef)):
            if Temperature_Coef[i] == 0:
                Temperature_Coef[i] = 100
        Ideal_Temperature=(Temperature_Coef.index(min(Temperature_Coef))+1)*5 - 2.5

        Humidity_Coef=Coef[13:17] 
        for i in range(len(Humidity_Coef)):
            if Humidity_Coef[i] == 0:
                Humidity_Coef[i] = 100
        Ideal_Humidity=(Humidity_Coef.index(min(Humidity_Coef))+1)*20 - 10

        Weather_Ideal_Var.set("Weather: {}, {}°C, {}% Humidity".format(Ideal_Weather,Ideal_Temperature,Ideal_Humidity))    #Update weather label

        Days_Coef=Coef[18:24]
        for i in range(len(Days_Coef)):
            if Days_Coef[i] == 0:
                Days_Coef[i] = 100
        Ideal_Day=days[Days_Coef.index(min(Days_Coef))]

        Time_Coef=Coef[25:48]
        for i in range(len(Time_Coef)):
            if Time_Coef[i] == 0:
                Time_Coef[i] = 100
        Ideal_Time=Time_Coef.index(min(Time_Coef))
        
        Day_Time_Ideal_Var.set("Day and Time: {} at {}:00".format(Ideal_Day,Ideal_Time))     #Update day and time labels
        
    
    Ideal_Window=Toplevel(window)
    Ideal_Window.title("Predict Ideal Conditions")
    Ideal_Window.geometry("400x500")                   #Create window with attributes
    Ideal_Window.grab_set()
    
    Ideal_Distance_Label=Label(Ideal_Window, text="Run Distance ",font=Label_Font,bd=0)
    Ideal_Distance_Label_2=Label(Ideal_Window, text="Distance: ",font=Button_Font,bd=0)      #Create Labels
    
    Ideal_Distance_Input=Spinbox(Ideal_Window,textvariable=Distance_Var,from_=0,to=100,width=10,format='%3.2f',increment=0.01)
    Ideal_Predict_Button=Button(Ideal_Window,image=Predict_Button_Photo,bg='#f0f0f0',relief=FLAT,width=150,height=54,bd=0,command=Predict_Ideal)    #Create button and input
    
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



Day_Time_Var = StringVar()
Day_Time_Label = Label(window, textvariable=Day_Time_Var,font=Label_Font,bd=0)            #Day and time label text variable and data
Day_Time_Var.set("Day and Time: ")

Distance_Var_2 = StringVar()
Distance_Label = Label(window, textvariable=Distance_Var_2,font=Label_Font,bd=0)            #Distance label text variable and data
Distance_Var_2.set("Distance: ")

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
Blank_Box=Label(Scrollbox,height=10,width=1)           #Place edit, add and delete buttons 
Scrollbox.place(x=1150,y=100)
Blank_Box.grid(row=0,column=1)

scrollbar.grid(row=0,column=0,sticky=NS)
List_Box.config(yscrollcommand = scrollbar.set)
List_Box_2.config(yscrollcommand = scrollbar.set)        #Set each list box to be based off the same scroll bar
List_Box_3.config(yscrollcommand = scrollbar.set)
List_Box_4.config(yscrollcommand = scrollbar.set)
def multiple_yview(*args):
    List_Box.yview(*args)
    List_Box_2.yview(*args)                  #Change the yview (scroll amount) of all listboxes with one function
    List_Box_3.yview(*args)
    List_Box_4.yview(*args)
    
scrollbar.config(command = multiple_yview)        #Connect scrollbar to listboxrd
List_Box_Frame_1.place(x=800,y=100)
List_Box_Frame_2.place(x=850,y=100)        #Place list box frames
List_Box_Frame_3.place(x=950,y=100)
List_Box_Frame_4.place(x=1050,y=100)
List_Box.pack()
List_Box_2.pack()                             #Place list boxes using pack method
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
window.mainloop()             #Run the program

#Existence check, Type Check, Range Check, Limited Choices
