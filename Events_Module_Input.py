import Datecheck_and_timecheck as Datecheck# todo  #2) check if there is overlap in the suration # include termination condition to come outta the program anytime in case of  anyput by mistake
import Extra_modules as extmod
import mysql.connector
import time # only function used is sleep
import threading # only the thread is used
mydb=mysql.connector.connect(host='localhost',user='root',password='lemonade1906',db="Cs_project_tes")#later change to Cs_project
curs= mydb.cursor()
# THE PROGRAM CAN ONLY DEAL WITH EVENTS IN ONE DAY
# does not check overlap of duration part
class Event  : # this is a definition of a new class called event
    def __init__(self):

        self.eventname="Rerun to rename"
        self.listofdays=[]
        self.dictofdays={}
        self.choice="N"
        self.date=""
        self.day=""
        self.alarm="Y"
        self.notes=""
        self.eventlength=60
        self.eventdetail=3
        self.time=None
        self.trialday = "" # just to get the day to check and ensure time doesnt overlap
        self.table_name_day_list = []
        self.invoke=0
        self.check_date_create=""
        self.converteddate_day_table_name=""
        self.tuple_converteddate=()
        self.bool=None
        self.date_list = []
        self.eventcode12 = ""
        self.eventname2 = ""
        self.alarm2 = ""
        self.notes2 = ""
        self.time2 = ''
        self.eventlength2 = 0
        self.eventdetail2 = 4
        self.dictofdays2 = {}
        self.listofautoinsert=[]
        self.n=None




    def inputdays(self): # this a function that gives pseudo variables for storing the day choices of the user

        for i in range(7):
            self.listofdays.append("day"+str(i))
        flag=False
        dayno=0
        while flag == False:
            try:
                dayno=int(input("Enter the number of days you wish the event to repeat in a week :"))# put a restriction of 7
                if dayno>7 or dayno<0:
                    print("Invalid input")
                    flag=False
                else:
                    flag=True
                print("\n")
            except ValueError :
                print("Invalid Input \n")
                flag=False
        # deletes the flag as it is no longer required
        for i in range(dayno):
            flag = False
            day = ""
            while flag==False:
                day = input("Enter a day: ")
                flag = extmod.check_input(day.upper(),"SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","")

            self.dictofdays[self.listofdays[i]]=day.upper() #the day choices of the user is stored as key value pairs
            print("\n")


    def inputdates(self): # this is a function that checks whether we need to have dates or days in the event
        flag = False
        while flag == False:
            print("Enter Y if you want it to be scheduled at a particular date,","Else enter N if you wish for it to repeat every week :",sep="\n")
            self.choice = str(input())
            print("\n")
            flag = extmod.check_input(self.choice.upper(),"Y","N")  # function from the module extra modules to check validity of input


    def eventdetails(self):# this provides personal customization option and personalised output in the final program
        print("Catergorize the event into any of the 3 catergories` : ")
        print("1) Work    2)Leisure    3)Others   4)fitness")
        print("\n")
        flag=False
        while flag==False:
            self.eventdetail = int(input("Enter 1, 2,3 or 4 as your choice: "))
            print(end="\n")
            flag=extmod.check_input(self.eventdetail,1,2,3,4)#this is a function from extra module which checks the validity of inputs


    def input_day_and_date(self):#this function asks the user for the choice between when he wishes the event to repeat
        if self.choice.upper()=="Y":
            flag=False
            while flag==False:
                self.date=input("Enter the date when you wish to schedule the event in YYYY-MM-DD :")
                print("\n")
                flag=Datecheck.datecheck(self.date)
        else:
            flag = False
            while flag == False:
                self.day=input("Enter Y if you wish of the event to repeat daily else enter N :")
                print("\n\n")
                flag = extmod.check_input(self.day.upper(), "Y", "N")
            if self.day.upper()=="Y" :# this a function that asks the user whether he wants to repeat the evnt every day
                self.dictofdays={"day0":"MONDAY","day1":"TUESDAY","day2":"WEDNESDAY","day3":"THURSDAY","day4":"FRIDAY","day5":"SATURDAY","day6":"SUNDAY"}
            else:
                self.inputdays()


    def alarms(self):# this takes in input to know if the user wants to be reminded when its time for the event
        flag=False
        while flag==False:
            self.alarm=input("Enter Y ig you wish to be reminded for the event else enter N :")
            print("\n\n")
            flag = extmod.check_input(self.alarm.upper(),"Y","N")
        self.alarm=self.alarm.upper()


    def eventlength1(self):
        flag = False
        while flag==False:
            self.eventlength=int(input("Enter how long you wish the event to be in minutes :"))
            print("\n\n")
            flag2=Datecheck.durationcheck(self.eventlength,self.time,self.date,self.trialday,self.dictofdays)
            if self.eventlength <0 and self.eventlength >1200 or flag2==False: # the max duration of an event is 20 hours
                print("Invalid Input for Event length, Please re enter")
                print("\n")

                flag=False
            elif flag2=="False1":
                self.eventtime()
                self.eventlength1()
                break
            else:
                flag=True


    def eventtime(self):
        flag=False
        while flag==False:
            self.time = input("Enter the time of the day when you wish to start the event (make sure to enter in the following format hh:mm:ss) :")
            print("\n\n")
            # the code from here is just to ensure that no date overlaps
            try:
                curs.execute("select weekday({});".format('"'+self.date+'"'))
                day_tuple = curs.fetchall()
                self.trialday = day_tuple[0][0]
            except: # solves the problem of overlappting time
                pass
            flag=Datecheck.Timecheck(self.time,self.date,self.trialday,self.dictofdays)

            if self.date!="" and self.choosetable(self.tuple_converteddate)==True:
                self.table_name_creator(self.date)
                print("Data processing please wait.........\n")
                self.tablecreate()
                self.inservalues_recurring2()
#                self.duplicate_remover()
                flag=Datecheck.Timecheck(self.time,self.date,self.trialday,self.dictofdays)






    def eventname_input(self):
        self.eventname = input("\nEnter the Name of Event: ")
        print("\n\n")
        self.eventname=self.eventname.rstrip().lstrip()


    def notes_input(self):
        self.notes=input("Enter Notes to be displayed regarding the event or any other link you wish to display during reminder call :")
        print("\n\n")
        self.notes.upper()

    def addevents(self) :  #  code to take input of the users events
        self.eventname_input()
        self.inputdates()
        self.input_day_and_date()
        self.notes_input()
        self.alarms()
        self.eventtime()
        self.eventlength1()
        self.eventdetails()


#*********************************************************************************************************************************************************************************************************88


    def current_time_generator(self):
        curs.execute("select curtime();")
        current_time=curs.fetchall()
        temp=str(current_time[0][0])
        if ':' in temp[0:2]:
            temp="0"+temp
        return temp

    def current_date_generator(self):# this function returns a value
        curs.execute("select curdate();")
        current_date=curs.fetchall()
        temp=str(str(current_date[0][0]).replace("-",""))# tuples are immutable
        return temp

    def table_name_creator(self, *date1):# this function is modified so as to fit the regular_table_creator
        if len(date1)==2  :# the parameters are always taken as a tuple
            curs.execute("select weekday({});".format('"'+date1[0]+'"'))
            day_tuple = curs.fetchall()
            day = day_tuple[0][0]
            self.check_date_create= Datecheck.name_createrandchanger(str(date1[0]), day)



        else:
            curs.execute("select weekday({});".format('"'+date1[0]+'"'))
            day_tuple=curs.fetchall()# returns a list of tuple of the day of week with monday as 0 and....... sunday as 6
            day=day_tuple[0][0]
            self.converteddate_day_table_name = Datecheck.name_createrandchanger(date1[0], day)  # this generates a unique table name based on each date
            self.tuple_converteddate = (self.converteddate_day_table_name,)


    def choosetable(self,tuple_date):# THis method helps us decide whether to create a new table or the table already exist
        showtable="show tables;"
        curs.execute(showtable)
        table_options=curs.fetchall()
        if tuple_date in table_options :
            return False
        else:
            return True
    def regular_table_creator(self):#this fuction is to create a new table regularly make sure to #todo schedule this to repeat regularly
        command = "Select adddate(curdate(),7);"
        curs.execute(command)
        obj = curs.fetchall()
        for i in range(len(obj)):
            self.table_name_creator(str(obj[i][0]),"null value")# the extra value is to induce the tuple
            self.bool=self.choosetable(self.check_date_create)# the date we get from the function table_name_creator first if statement
            if self.bool==True :
                self.invoke=1  # this flag variable helps me induce the tablecreate every day to create a new table
                self.tablecreate()
                self.invoke=0




    def tablecreate(self):# this a function to create a table and it only creates the table if the table is already not created
        #Date date ,Day varchar(200)
        if  self.date=="" or self.invoke==1 :#when the entry was to be repeated every week

            for i in range(7):# creates schedules for the next 7 days
                command="Select adddate(curdate(),{});"
                curs.execute(command.format(i))
                obj=curs.fetchall()
                self.date_list.append(str(obj[0][0]))
            for i in range(7):
                self.table_name_creator(self.date_list[i])
                flag=self.choosetable(self.tuple_converteddate)
                if flag==True:
                    createtable = "Create table {} (Event_Name varchar(50),Alarm char not null, notes varchar(120), Time varchar(30), Duration integer(4), Detail varchar(10)); "
                    curs.execute(createtable.format(self.converteddate_day_table_name,))# try adding quotes
                    mydb.commit()

                    self.table_name_day_list.append(self.converteddate_day_table_name)# list of all the table names created

                else:
                    pass


        elif self.date != "":
            self.table_name_creator(self.date)  # create a table name using the function to create names using the date entered
            flag = self.choosetable(self.tuple_converteddate)
            if flag == True:
                createtable = "Create table {} (Event_Name varchar(30),Alarm char not null,notes varchar(120),Time varchar(8),Duration integer(4),Detail varchar(10));"
                curs.execute(createtable.format(self.converteddate_day_table_name))
                mydb.commit()
            else:
                pass




    def data_file_daywise(self):# invoke in init # check this part
        f1=open("Data_regarding_daily_events","a")
        data_list=[self.eventname, self.alarm, self.notes, self.time, self.eventlength, self.eventdetail,self.dictofdays]#self.eventlength and event detail are not str and int
        for i in range(len(data_list)-1):
              f1.write(str(data_list[i])+"\n")
        f1.write("#"+"\n")
        for j in range(len(self.dictofdays)):
            f1.write(self.dictofdays["day"+str(j)]+"\n")
        f1.write("*"+"\n")
        f1.close()

    def insertvalues_date_day_everyday(self,table_name,eventname,alarm,notes,time,eventlength,eventdetail):# this function helps to insert the values inputted from the user into the table
        self.tableinsert="insert into {} values({},{},{},{},{},{});"
        curs.execute(self.tableinsert.format(table_name,"'" + str(eventname)+"'","'"+ str(alarm)+"'","'"+ str(notes)+"'","'"+ str(time)+"'", eventlength,"'"+ str(eventdetail)+"'"))
        mydb.commit()# time is of data type varchar 

    def insertvalues(self):# call this

        if self.date !="" :

            self.insertvalues_date_day_everyday(self.converteddate_day_table_name, self.eventname, self.alarm, self.notes, self.time, self.eventlength, self.eventdetail)

        else:
            self.data_file_daywise()
            self.temp_list=[]  # to ensure events are added only to future dates # dates of the week where it is the days entered by the user is chosen
            temp_list2=[]# this is the first round of selection where future dates are chosen
            curs.execute("show tables;")
            obj=curs.fetchall() # this returns a  list of tuples
            current_date=self.current_date_generator() # UDF which uses sql to get the current date
            for i in range(len(obj)):
                date=(obj[i][0][0:8]) # this extracts the date from each table name
                if int(current_date)<= int(date) :#checks if the table to which data is being added is for today's schedule or futures and not pasts
                    temp_list2.append(obj[i])
                else:
                    pass

            for i in range(len(temp_list2)):# traverses though all the potential dates
                   for j in range(len(self.dictofdays)):#traverses through all the days it has to add to like sunday, monday etc
                    if temp_list2[i][0][10:]==self.dictofdays["day"+str(j)]:# this checks the day from each of the names and then chooses whether to insert into that
                        self.temp_list.append(obj[i][0])

            for i in range(len(self.temp_list)):# temp_list stores the list of tables names to which we need to add the data
                self.insertvalues_date_day_everyday(self.temp_list[i], self.eventname, self.alarm, self.notes, self.time, self.eventlength, self.eventdetail)



    def insertvalues_recurring(self):# this function extracts data from the datafile and then reassigns values to them for reinsertion
        f1 = open("Data_regarding_daily_events", "r")
        self.reccur=1 # condition value
        temp_list=f1.readlines()
        self.main_list=[]
        self.e=-1     # i make them class variables so as to remove the problem of the variable scope
        while True:# this loops reads the data from the data file and stores it as a main list
            secondary_list = []
            self.dictofdays2={}
            for i in range(self.e+1,len(temp_list)):
                if temp_list[i].rstrip("\n") !="*" and temp_list[i].rstrip("\n") !="#" :
                    secondary_list.append(temp_list[i].rstrip("\n"))

                elif temp_list[i].rstrip("\n")== "#":# need to include some sort of continue or pass statementt
                    self.n=i+1

                elif temp_list[i].rstrip("\n")=="*":
                    self.e=i
                    break

            i=0
            secondary_list=secondary_list[0:6]
            for k in range(self.n,self.e):
                i=i+1# just to create the necessary key pairs to store value
                self.dictofdays2["day"+str(i)]=temp_list[k].rstrip('\n')
            secondary_list.append(self.dictofdays2)
            self.main_list.append(secondary_list)# the main list is a list of all records where each record is a list
            if self.e==len(temp_list)-1 :
                break



    def inservalues_recurring2(self): # call this
        global temp_list
        self.insertvalues_recurring()
        temp_list = []  # to ensure events are added only to future dates
        temp_list2 = []
        curs.execute("show tables;")
        obj = curs.fetchall()  # this returns a  list of tuples
        current_date = self.current_date_generator()  # UDF which uses sql to get the current date
        for i in range(len(obj)):
            date = (obj[i][0][0:8])
            if int(current_date) <= int(date):
                temp_list2.append(obj[i]) # list of future dates
            else:
                pass# main list contains 3 litsts to be added # PROGRAM WORKS FINE TILL HERE
        for k in range(len(self.main_list)):# list of all the records where each record is a list # loop of 3 lists
            temp_list = []
            for i in range(len(temp_list2)):# list of all the dates to which we wanna add it is a list of tuples where the tablenames are stores in the first index of the tuple
                    for j in range(len(self.main_list[k][6])):# will traverse through the dict of days for a particular entry

                            if temp_list2[i][0][10:] == self.main_list[k][6]["day" + str(j+1)]:  # this checks the day from each of the names and then chooses whether to insert into that
                                temp_list.append(temp_list2[i][0])#make chnages


            self.eventname2, self.alarm2, self.notes2, self.time2, self.eventlength2, self.eventdetail2= self.main_list[k][0:6]

            for i in range(len(temp_list)):# temp_list stores the list of tables names to which we need to add the data
                if self.check_self_insert(temp_list[i],k) == True:
                    self.insertvalues_date_day_everyday(temp_list[i], self.eventname2, self.alarm2, self.notes2, self.time2, self.eventlength2, self.eventdetail2)

    def duplicate_remover(self):
        curs.execute("show tables;")
        self.alltables=curs.fetchall()
        for i in range(len(self.alltables)):# list of tuples

            command="Create table Duplicate (Event_Name varchar(30),Alarm char not null,notes varchar(120),Time varchar(8),Duration integer(4),Detail varchar(10));"
            curs.execute(command)
            mydb.commit()
            command="select distinct * from {};"
            curs.execute(command.format(self.alltables[i][0]))
            enteries =curs.fetchall() # list of tuples of enteries
            for j in range(len(enteries)):
                self.insertvalues_date_day_everyday("Duplicate",enteries[j][0],enteries[j][1],enteries[j][2],enteries[j][3],enteries[j][4],enteries[j][5])
            curs.execute("drop table {};".format(self.alltables[i][0]))
            mydb.commit()
            curs.execute("Alter table Duplicate rename to {};".format(self.alltables[i][0]))
            mydb.commit()
        self.alltables=None # since it is no longer required
    def table_clearer(self):
        curs.execute("Show tables;")
        namelist=curs.fetchall()
        current_date=self.current_date_generator()
        temp_list=[]
        for i in range(len(namelist)):
            if int(namelist[i][0][0:8])< int(current_date):
                temp_list.append(namelist[i][0])
        for i in range(len(temp_list)):
            curs.execute("Drop table {}".format(temp_list[i]))
            mydb.commit()





#this is not working properly SO THID FUNCTION IS CURRENTLY UNUSED
    def check_self_insert(self,tablename,index): # this function is to check if a record already exists
        command="Select * from {};"
        curs.execute(command.format(tablename))
        data_list=curs.fetchall()


        for i in range(len(data_list)):# since data_list also has
            templist=[int(self.main_list[index][4]),self.main_list[index][5]]
            if data_list[i]==tuple(self.main_list[index][0:4]+(templist)):
                return False
            else:
                pass
        return True



    def class_autocall(self):
        print("Data is being added into database... please wait......\n")
        self.tablecreate()
        self.insertvalues()



class Simultaneous(Event,threading.Thread):
    def __init__(self) :
        Event.__init__(self)
        threading.Thread.__init__(self)
        self.table_clearer()
    def run(self):     # this method will run in a different thread in the background continuously
        seconds = 59
        self.regular_table_creator()
        self.inservalues_recurring2()
        self.table_clearer()
#        print("\n\nTHREAD 2 IS RUNNING\n\n")# todo REMEMBER TO REMOVE AS JUST ADDED FOR TESTING
        while True:  # this makes the event run everyday at midnight
            currenttime = self.current_date_generator()
            if currenttime[0:5] == "00:00":
                self.regular_table_creator()
                self.inservalues_recurring2()
                self.table_clearer()
                time.sleep(60*60)

            time.sleep(seconds)  # loop runs every 59 secs # the reason so as to save memory space but comes with the tradeoff of seconds


# create a diff file which will always run in the background
# in recurring i use already assigned values and automatic name generator automatically generated files

#obj1=Event()
#obj1.addevents()
#obj1.class_autocall()
#time.sleep(1)
#thr2=Simultaneous()
#thr2.start()













