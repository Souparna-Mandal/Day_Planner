import Datecheck_and_timecheck as Datecheck
import Extra_modules as ext_mod
import mysql.connector
import Events_Module_Input as mainmod
mydb=mysql.connector.connect(host='localhost',user='root',password='lemonade1906',db="Cs_project_tes")#later change to Cs_project
curs= mydb.cursor()


class Output :# this a fuction to give the user output to the various details stored in the sql servers
    def __init__(self):
        self.tablename="" # this is a class variable which has varying value in every function so make sure to change it in every fuction
        self.inputeddate=None
        self.details=["WORK","LEISURE","OTHERS","FITNESS"]
        curs.execute("select curdate()")
        var=curs.fetchone()
        self.currentdate=str(var[0])


    def table_name_setter(self, tabledate): # date is the defining property and is used to extract or create the table name when provided with a date
        curs.execute("select weekday('{}');".format(tabledate))
        day_tuple = curs.fetchall()
        day = day_tuple[0][0]
        self.tablename = Datecheck.name_createrandchanger(tabledate, day)


    def check_schedule_availibility(self,date):# this function checks whether the schedule for a particular function exists or not
        self.table_name_setter(date)
        command="show tables;"
        curs.execute(command)
        tables_tuple=curs.fetchall()
        if (self.tablename,) in tables_tuple :
            return True
        else:
            return False
    def fixed_length(self,text,length):
        if len(text)>length:
            text=text[:length]
        elif len(text)<length:
            text=(text+" "*length)[:length]
        return (" "+text)

    def show_schedule(self,command,ind_var): # this function is to show the data in a days schedule

        curs.execute(command.format(self.tablename)%ind_var)# remember to reset self.tablename in every function and also also include the % and pass ind_var(inducing variable) as a tuple
        datatuple=curs.fetchall()
        print("*"*139)
        print("*",self.fixed_length("Sl_no",7),self.fixed_length("Event Name",18),self.fixed_length("Notes",60),self.fixed_length("Starting Time",15),self.fixed_length("Duration",10),self.fixed_length("Type of Event",14),"*", sep="*")
        print("*" * 139)
        for i in range(0,len(datatuple)):
            detail = self.details[int(datatuple[i][4])-1]
            print("*",self.fixed_length(str(i+1),7),self.fixed_length(str(datatuple[i][0]),18),self.fixed_length(str(datatuple[i][1]),60),self.fixed_length(str(datatuple[i][2]),15),self.fixed_length(str(datatuple[i][3]),10),self.fixed_length(detail,14),"*",sep="*")
        print("*" * 139)




    def show_todays_schedule(self):
        flag=self.check_schedule_availibility(self.currentdate)
        if flag== True:
            self.table_name_setter(self.currentdate)
            self.show_schedule(command="select Event_name,%s,Time,Duration,Detail from {}",ind_var=("notes",))# i have done it this way so i can keep using the same call function for later outputs
        else:
            print("There are no events scheduled for today ")

    def show_anydays_schedule(self):
        flag=False
        while flag==False:
            self.inputeddate=input("Enter the date for which you want to check schedule in yyyy-mm-dd")
            flag=Datecheck.datecheck(self.inputeddate)#todo i may want to add a facility later to go back to the previous menu


        flag=self.check_schedule_availibility(self.inputeddate)
        if flag== True:
            self.table_name_setter(self.inputeddate)
            self.show_schedule(command="select Event_name,%s,Time,Duration,Detail from {}",ind_var=("notes",))

        else:
            print("There are no events scheduled for this day")
            print("Please add events to view them")

    def show_schedule_via_name(self): # this calls out all the data regarding a particular event
        print("\n")
        name=input("Enter the Name of the event which you wish to view: ")
        print("\n")
        name=name.rstrip().lstrip()
        command="Select Event_name,notes,Time,Duration,Detail from %s where Event_Name='{}';"
        curs.execute("show tables;")
        table_name=curs.fetchall()
        required_days=[]

        flag=0
        for i in range(len(table_name)):

            curs.execute(command.format(name)%(table_name[i][0],))
            data=curs.fetchone()

            if data!=None:
                self.tablename=table_name[i][0]#eg of table name 20201026s_SUNDAY # that is why the slices are done so
                required_days.append(self.tablename[10:])
                flag=flag+1


        if flag==0:
            print("There is no such event")
            return

        self.show_schedule(command="select Event_name,notes,Time,Duration,Detail from {} Where Event_Name='%s'",ind_var=(str(name),))

        print("The day/days on which the event is repeated is/are ",end="")
        for i in range(len(required_days)):
            print(required_days[i],end=", ")


    def show_schedule_via_time(self):
        global time
        while True:
            time=int(input("Enter The time when you wish to check events: "))
            if Datecheck.Timecheck(time=time,checker_var=1)==True:
                break
        time=Datecheck.integertimegenrator(time)
        curs.execute("Select Time,Duration,Event_Name from {}")
        data=curs.fetchall()
        for i in range(len(data)):
            begintime=Datecheck.integertimegenrator(data[i][0])# gets the begin time of an event in integer
            endtime=Datecheck.integertimegenrator(Datecheck.addtimes(data[i][1],begintime))# will make it integer and get the time requiredor the end time of an event in integer
            if time>begintime and time< endtime:
                self.table_name_setter(self.currentdate)
                print("The event scheduled for today are as follows")
                self.show_schedule(command="Select Event_name,%s,Time,Duration,Detail from {} where Event_Name=%s",ind_var=(data[i][2]))

    def autoouput(self):
        print("\n\nPLEASE ENTER HOW YOU WISH TO VIEW YOUR SCHEDULE:\n\n\n")
        print("1) DISPLAY TODAY'S SCHEDULE:\n\n2) DISPLAY A PARTICULAR DAY'S SCHEDULE USING DATE:\n\n3) DISPLAY EVENTS VIA THEIR NAME:\n\n4) DISPLAY EVENTS AT A PARTICULAR TIME (shows output for current date):\n\n ")
        choice=int(input("ENTER YOUR CHOICE FROM 1 TO 4: "))
        if choice==1:
             self.show_todays_schedule()
        elif choice==2:
             self.show_anydays_schedule()
        elif choice==3:
             self.show_schedule_via_name()

        elif choice==4:
             self.show_schedule_via_time()
        else:
             print("Invalid Input Please Re Enter")
             self.autoouput()





class Update(Output):
    def __init__(self):
        Output.__init__(self)
        self.data_list=["Event_Name","Alarm","Notes","Time","Duration","Detail"]

    def Update_details_datewise(self):
        flag=False
        while flag==False:
            self.date_choice=input("Enter the Day you would like to Update the Event in yyyy-mm-dd : ")
            print("\n\n")
            flag=Datecheck.datecheck(self.date_choice)
        self.table_name_setter(self.date_choice)
        try:
            self.show_schedule(command="select Event_name,%s,Time,Duration,Detail from {}",ind_var=("notes",))
        except mysql.connector.Error: # catches all mysql errors
            print("There Are No Events Schedule For This Day\n\n")
        flag=False
        while flag==False:
            print("\n\n Enter the Sl_NO of the event you would like to Update:")
            try :
                self.choice2=int(input())
                flag=True
            except ValueError:
                print("\n\nIncorrect Input for SL_NO\n\n")
                flag=False
        #self.delete_event(date,event_name)
       # return(True)# if this comes True then run the Input and insert commands
        print("\n\nEnter the attributes you would to edit from the Following:\n\n1) Event_Name\n\n2) Alarm \n\n3) Notes \n\n4) Time \n\n5) Type\n\n6) Duration ")#todo edit this
        list=[]
        for i in range(1,7):
            try :
                num=int(input("\n\nEnter your choice (Please not to enter an integer from 1 to 5)\nElse Enter 0 when you have entered all the attributes you wish to change :"))
                if num not in list and num>=1 and num<=6 :
                    list.append(self.data_list[num-1])
                elif num==0:
                    break
            except ValueError:
                print("The Input Is Invalid, Please re Enter your Choice")
        curs.execute("Select * from {};".format(self.tablename))
        self.data_of_record=curs.fetchall()
        curs.execute(("Delete from {} where Event_name='{}' and Time='{}';".format(self.tablename,self.data_of_record[0][0],self.data_of_record[0][3])))
        mydb.commit()
        obj1=mainmod.Event()
        if "Event_Name"in list :  # did not use elif as i want it to check all conditions
            obj1.eventname_input()
            self.eventname=obj1.eventname

        else:
            self.eventname=self.data_of_record[0][0]


        if "Notes"in list:
             obj1.notes_input()
             self.notes=obj1.notes

        else:
            self.notes=self.data_of_record[0][2]


        if "Alarm"in list:
            obj1.alarms()
            self.alarms=obj1.alarm

        else:
            self.alarms=self.data_of_record[0][1]


        if "Time"in list:
            obj1.eventtime()
            self.time=obj1.time


        else:
            self.time=self.data_of_record[0][3]


        if "Duration" in list:
            obj1.eventdetails()
            self.detail=obj1.eventdetail# its an integer wont cause issue


        else:
            self.detail=self.data_of_record[0][4]

        if "Detail" in list:
            obj1.eventlength1()
            self.duration = obj1.eventlength

        else:
            self.duration = self.data_of_record[0][5]


        curs.execute("Insert into {} values('{}','{}','{}','{}',{},'{}');".format(self.tablename,self.eventname,self.alarms,self.notes,self.time,self.duration,self.detail))
        mydb.commit()
        print("Your Updated Table is :")
        #self.tablename will be used
        self.show_schedule(command="select Event_name,%s,Time,Duration,Detail from {}", ind_var=("notes",))










    def Update_Details(self):

        flag=False
        while flag==False:
            self.choice=input("\n\nWould you like to:\n\n1) Update the event on a particular Day \n\n2)Update all occurrences of the Event\n")
            flag=ext_mod.check_input(self.choice,'1','2')
        if self.choice=='1':
            self.Update_details_datewise()
        elif self.choice=='2':
            print("That Feature is Under Development")

    def Delete_Details(self):
        global choice3
        flag = False
        while flag == False:
            self.date_choice = input("Enter the Day you would like to Update the Event in yyyy-mm-dd : ")
            flag = Datecheck.datecheck(self.date_choice)
        self.table_name_setter(self.date_choice)
        try:
            self.show_schedule(command="select Event_name,%s,Time,Duration,Detail from {}", ind_var=("notes",))
            flag=False
            while flag==False:
                print("\n\n Enter the Sl_NO of the event you would like to DELETE:")
                try :
                    self.choice3=int(input())
                    flag=True
                except ValueError:
                    print("\nIncorrect Input for SL_NO\n")
                    flag=False

                curs.execute("select * from {}".format(self.tablename))
                temp_var = curs.fetchall()
                temp_data = temp_var[self.choice3 - 1]
                curs.execute(("Delete from {} where Event_name='{}' and Time='{}';".format(self.tablename,temp_data[0],temp_data[3])))
                mydb.commit()
                print("\nEvent Sucessfully Deleted\n")
        except mysql.connector.Error:
            print("\nThe Schedule for this day does not exist\n")














        



























    # fuction to view world specific or detail specific tasks
    # fuction to view the grapgh of the work completed
    #display the schedule for the entire week

