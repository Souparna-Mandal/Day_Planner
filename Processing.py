import mysql.connector
import Events_Module_Input
import Datecheck_and_timecheck as Datecheck
import Extra_modules as extmod
import matplotlib.pyplot as matplotlib
import time
mydb=mysql.connector.connect(host='localhost',user='root',password='root',db="Cs_project_tes")#later change to Cs_project
curs= mydb.cursor()

class Processing():# the thread is to run the program that checks for event time in parallel
    def __init__(self):
        self.curdate=""
        self.tablename=""
        self.curtime= ""
        self.records=[]
        self.eventtype={1:"WORK",2:"LEISURE",3:"OTHERS",4:"FITNESS"}
        self.end=[]
        self.recurchoice=""

    def current_date_time_getter(self): # gets the current time and date

        obj=Events_Module_Input.Event()
        self.curdate=obj.current_date_generator()
        self.curtime=obj.current_time_generator()


    def current_table_name(self):# gets the table name for the current day
        self.current_date_time_getter()
        curs.execute("select weekday({});".format('"' + self.curdate + '"'))
        day_tuple = curs.fetchall()
        day = day_tuple[0][0]
        self.tablename = Datecheck.name_createrandchanger(self.curdate, day)

    def fixed_length(self,text,length):
        if len(text)>length:
            text=text[:length]
        elif len(text)<length:
            text=(text+" "*length)[:length]
        return text

    def eventtime(self,index):# this functions has all the details to be printed
        print("\n\n\n\n\n\n\nIT IS TIME FOR YOUR EVENT\n\n")
        print("The Current Time is :", self.curtime)
        list1=["Event Name","Type of Event","End Time","Notes regarding Event"]
        print("|"*(20*4+5))
        print("|", end="")
        for i in list1:
            print(self.fixed_length(i,20),end="|")
        print("|" * (20 * 4 + 5))
        endtime=Datecheck.addtimes(self.records[index][4], self.records[index][3])# adds time from the datecheck and timecheck module takes duration, time as input
        print("|",self.fixed_length(self.records[index][0],20),"|",self.fixed_length(self.eventtype[int(self.records[index][5])],20),"|",self.fixed_length(endtime,20),"|",self.fixed_length(self.records[index][2],20),"|","\n",sep="")
        print("|"*(20*4+5))# change accordingly
        self.end.append([self.records[index][0],endtime]) # this will a list of all the events currently running passes in event name and endtime

        # call the audio


    def schedule_changer(self,tablename):

        command="Update {} set Time=Addtime(Time,'00:10:00') where Event_Name not in '{}'and Addtime(Time,'00:10:00')<='24:00:00';"
        command2="Select Event_name from {} where Time<curtime()"# i used not in
        curs.execute(command2.format(tablename))
        required_time=curs.fetchall()# list of tuples

        curs.execute(command.format(tablename,(required_time[0])))# directly passes tuple for comparison
        mydb.commit()

        for i in range(len(self.records)):# this changes the durations which crosses end of the day
            testtime = Datecheck.addtimes(10+self.records[i][4], self.records[i][3])# checks if adding 10 mins makes the time pas 24:00:00
            if Datecheck.integertimegenrator(testtime)>Datecheck.integertimegenrator("24:00:00"):
                command="Update {} set Time='24:00:00' where Event_Name={};"
                curs.execute(command.format(tablename,self.records[0]))# work over here
                mydb.commit()



    def eventend(self,index):# program cant deal with one exception

        print("\n\nThe allotted Time for the Event ",self.end[index][0]," is up would you like to extend the event by 10 minutes ?\n")
        flag=False
        while flag==False:
            self.recurchoice=input("Enter your choice (y/n) : ")
            self.recurchoice=self.recurchoice.upper()
            flag=extmod.check_input(self.recurchoice,"Y","N")# make changes to self.end

        if self.recurchoice.upper()=="Y":
            print("\nPlease note all your forth coming events will be adjusted accordingly.\n") # eventname has the day we will be using that
            newendtime=Datecheck.addtimes(10,self.end[index][1])
            bool=Datecheck.reccurtime(newendtime,{},self.curdate,self.end[index][0][10:])# calls the func from datecheck the 3rd parameter is the day of the week
            if bool==False:# first it checks if adding 10 mins to the current time disrupts the other events
                self.schedule_changer(self.tablename)
                self.end[index][1]=Datecheck.addtimes(10,self.end[index][1])
            else:
                curs.execute("Update {} set Time=Addtime(Time,'00:10:00') where Event_Name='{}';".format(self.tablename,self.end[index][0]))# not perfect logic
                self.end[index][1] = Datecheck.addtimes(10, self.end[index][1])


        if self.recurchoice.upper()=="N":
            print("THE EVENT ",self.end[index][0]," HAS SUCCESSFULLY COME TO AN END, HERE IS A PIE CHART OF ALL THE ACTIVITES SO FAR PLANNED FOR TODAY")
            self.dataanalysis()





    def autorun(self):# this is the main function
        self.current_table_name()
        command="Select * from {}"



        curs.execute(command.format(self.tablename))
        self.records = curs.fetchall()  # this is a list of tuples of all records

        for i in range(len(self.records)):
                self.current_date_time_getter()

                if self.records[i][3][0:6]== self.curtime[0:6] and self.records[i][1]=="Y": # the condition to check if its time for an event to begin and if alarms is Y

                    self.eventtime(i)
                    time.sleep(60)



                if self.end !=[]:
                    for j in range(len(self.end)): # this checks from the list of current running events if any event has finished
                        if self.end[j][1][0:6]== self.curtime[0:6]:# condition to check if its time for an event to end

                            self.eventend(j) # it"""


#            time.sleep()



    def dataanalysis(self): # this function prints a pie chart at the end of the day showing the work results
        curs.execute("Select sum(Duration),Detail from {} group by Detail;".format(self.tablename))
        detaillist=[]
        labels=[]
        records=curs.fetchall()
        for i in range(len(records)):
            detaillist.append(records[i][0])
            labels.append(self.eventtype[int(records[i][1])])



        matplotlib.pie(detaillist,labels=labels,autopct="%1.1f%%")
        matplotlib.show()




