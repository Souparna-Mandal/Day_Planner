import mysql.connector
import math
mydb=mysql.connector.connect(host='localhost',user='root',password='xxxxxx',db="Cs_project_tes")#later change to Cs_project
curs= mydb.cursor()

def datecheck(date):# a fuction to check if date input is correct needs improvement in leap year and number of days
    date=date.rstrip()
    date=date.lstrip()
    year=date[0:4]#makes sure to separate the day part from the date
    month=date[5:7]
    day=date[8:10]
    flag=0# date is like this 2020-09-09
    try:
        if int(day)<32 and int(day)>0:
            flag=flag+1
        if int(month)<13 and int(month)>0:
            flag=flag+1
        if int(year)>=1900 and int(year)<2100:
            flag=flag+1
        if date[4]=="-" and date[7]=="-":
            flag=flag+1
    except ValueError:
        pass
    finally:
        if(flag==4):
            return True
        else:
            print("Invalid Input of date, Please re enter")
            print("\n")
            return False

list_of_days_of_week=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]


def minute_time_converted(minutes):  # this program converts the duration of the program from minutes to hours and minutes and seconds
    global mins
    global hour
    hour= str(minutes // 60)
    mins= str(int(math.floor(minutes % 60)))
    if len(str(hour)) != 2:
        hour = "0" + str(hour)
    if len(str(mins)) != 2:
        mins = "0" + str(mins)
    return (hour + ":" + mins + ":" + "00").rstrip().lstrip()


def addtimes(minutes, starttime):# this program ( adds minutes to a time)
     timeadd=minute_time_converted(minutes)
     command="select Addtime('{}','{}');"
     curs.execute(command.format(starttime,timeadd))
     time=(curs.fetchall())
     return(str(time[0][0]))



def name_creater(date, day):# this fuction will be utilized in the sql link module for aiding in the table names
    date=date.rstrip()
    date=date.lstrip()# day passed there is a number
    date=date.replace('-','')+"s"+"_"+day #eg of table name 20201026s_SUNDAY # we need to call from list
    return date
def name_createrandchanger(date,day):
    return(name_creater(date,list_of_days_of_week[day]))

def integertimegenrator(time):# of the form hh:mm:ss # comparing it in integer form or time form wont make any difference
    timepart1=time[0:2]
    timepart2=time[3:5]
    timepart3=time[6:8]
    return(int(timepart1+timepart2+timepart3))


def current_date_generator():# this function returns a value IN INTEGER FORM FOR CURRENT DATE
       curs.execute("select curdate();")
       current_date=curs.fetchall()
       temp=str(str(current_date[0][0]).replace("-",""))# tuples are immutable
       return temp


def reccurtime(time,dict_days,date="",day="",):# this function checks if the time inputed is in the same time as another scheduled event
    global endtime
    global starttime
    if date !="":

        tablename=name_creater(date,day)
        record="Select Time,Duration from {};"
        try:
            curs.execute(record.format(tablename))
            list_time=curs.fetchall()
            if len(list_time)!=0:# this condition means there are 0 records in the table
                time = integertimegenrator(time)
                for x in range(len(list_time)):
                    endtime=addtimes(list_time[x][1], list_time[x][0]) # converts time to integer form
                    endtime=integertimegenrator(endtime)
                    starttime=integertimegenrator(list_time[x][0])

                    if time>=starttime and time<=endtime:
                        return False
                return True

            else:
                return True
        except mysql.connector.Error: # catches all mysql syntax related errors
            return True

    else:
            global temp_list2  # to ensure events are checked with future dates # dates of the week where it is the days entered by the user is chosen
            temp_list2 = []  # this is the first round of selection where future dates are chosen
            curs.execute("show tables;")
            obj = curs.fetchall()  # this returns a  list of tuples
            current_date = current_date_generator()  # UDF which uses sql to get the current date
            for i in range(len(obj)):
                date = (obj[i][0][0:8])  # this extracts the date from each table name
                if int(current_date) <= int(date):  # checks if the table to which data is being added is for today's schedule or futures and not pasts
                    temp_list2.append(obj[i])
                else:
                    pass

            time = integertimegenrator(time) # converts the given time to integer
            for i in range(len(temp_list2)):
                for j in range(len(dict_days)):
                    if dict_days["day"+str(j)] in temp_list2[i][0]:

                        record = "Select Time,Duration from {};"
                        curs.execute(record.format(temp_list2[i][0]))
                        list_time = curs.fetchall()
                        if len(list_time)!=0:
                            for x in range(len(list_time)):
                                endtime = addtimes(list_time[x][1], list_time[x][0])
                                endtime = integertimegenrator(endtime)
                                starttime = integertimegenrator(list_time[x][0])


                                if time >= starttime and time <= endtime:
                                    return False
                                else:
                                    pass

                        else:
                            return True # because the schedule is empty means we can add events

            return True







def Timecheck(time=None,date=None,day=None,dict_days=None,checker_var=0):#this a fuction that checks whether the time inputed by the user is valid
    time=time.lstrip()
    time=time.rstrip()
    hour=time[:2]
    minute=time[3:5]
    second=time[6:]
    flag=0      #13:23:12
    try:
        if int(hour)<25 and int(hour)>=0:
            flag=flag+1
        if int(minute)<61 and int(minute)>=0:
            flag=flag+1
        if int(second)>=0 and int(second)<61:
            flag=flag+1
        if time[2]==":" and time[5]==":":
            flag=flag+1
        if checker_var==1: # checker var is useful only for the output module
            if flag==4:
                return True
            else:
                print("Invalid Input of Time")
                return False
        try:
            if reccurtime(time,dict_days,date,list_of_days_of_week[int(day)])==True:
                flag=flag+1
            else:
                 print("There is already an event schedule in the time entered, please enter another time")

        except TypeError: # comes up when day= None type which is when we take repetition weekly option
            if reccurtime(time=time,dict_days=dict_days)==True:
                flag=flag+1
            else:
                 print("There is already an event schedule in the time entered, so ")
    except ValueError:
        pass
    finally:
        if(flag==5):
            return True
        else:
            print("Invalid Input of time, Please re enter")
            print("\n")
            return False

def durationcheck(duration,time,date,day,dict_ofdays):# checks the duration vality   # NOTE THERE IS ONE CASE WHICH WILL NOT BE CHECKED
    finaltime=addtimes(duration,time)
    flag = Timecheck(finaltime, date, day, dict_ofdays)
    finaltime=integertimegenrator(finaltime)

    if finaltime >240000 :
        print("The event will go on past midnight onto a new day which is not allowed")
        return False
    if flag==False:
        print("The event overlaps with another reenter the details accordingly:")
        return "False1"
    return True

def date_backconverted(name):# this fuction just takes in a table name and extracts the date from it
    name.rstrip()
    name.lstrip()
    name = name[0:5]+"-"+name[5:7]+"-"+name[7:9]
    return(name)

def date_creator(date):# this function just takes in a date and converts it to an integer form for comparison
    date.rstrip()
    date.lstrip()
    date=date.replace('-','')
    return(date)



