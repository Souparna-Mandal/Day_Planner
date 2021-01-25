import Events_Module_Input as recur
import time
object1=recur.database()
seconds=30*60
object1.regular_table_creator()
object1.inservalues_recurring2()
while True:# this makes the event run everyday at midnight
    currenttime = object1.current_date_generator()
    if currenttime[0:5]=="00:00" :
        object1.regular_table_creator()
        object1.inservalues_recurring2()
    time.sleep(seconds)# loop runs every 30 mins
