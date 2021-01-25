import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='lemonade1906',db="Cs_project_tes")#later change to Cs_project
curs= mydb.cursor()

def check_input(invar, *condition) :# the star makes it a variable length arguement #checks for validity of input
    if invar in condition:
        return True
    else:
        print("Please re enter as input is invalid")
        print("\n")
        return False

#NOT USEFUL ANYMORE AS I HAVE REMOVED EVENTCODE
def event_code_generator(date_converted):# this method generates a unique event code for each event by adding a number to the current date


    curs.execute("Select count(*) from {}".format(date_converted))
    slno=curs.fetchall()[0][0]
    eventcode = date_converted + str(slno+1)
    return eventcode                        # generates a unique event code






