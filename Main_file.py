import threading
import Events_Module_Input as inmod
import Processing as process
import Events_Module_output as outmod
import time

with open("checker.txt", "w") as f1:
    f1.write("N\n")
print("*********************************ASIAN INTERNATIONAL PRIVATE SCHOOL RUWAIS********************************************")
print("*******************************************RUWAIS ABU DHABI***********************************************************")
print("\t\tWELCOME TO YOUR DAY PLANNER\n\t\tUSE THIS TO PLAN YOUR DAY EFFICIENTLY\n\t\tFOLLOW THE ON SCREEN PROMPTS\n\t\tENJOY\n")
print("\t\tPlease wait patiently as the initial setup may take up to 1 minute\n\t\tDO NOT CLOSE THE PROGRAM!!\n\n\n\n\n\n\n")
thread1=inmod.Simultaneous()
thread1.setDaemon(True)
thread1.start()# starts the backgroup process of autocreating tables and inserting daily events
time.sleep(1)
processing=process.Processing()
processing.setDaemon((True))
processing.start()
time.sleep(0.1)



#class MAINCLASS(threading.Thread):
#    def __init__(self):
#        threading.Thread.__init__(self)
#    def run(self):
while True:
    try:
        with open("checker.txt","r") as f1:
            flag=f1.readline().rstrip("\n")
            while flag=="Y":
                time.sleep(1)
                if flag=="N":
                    continue
    except IOError:
        continue

    print("CHOOSE ANY OF THE FOLLOWING:\n\n")
    print("1) SCHEDULE A NEW EVENT\n")
    print("2) DISPLAY SCHEDULED EVENTS\n")
    print("3) UPDATE SCHEDULED EVENTS\n")
    print("4) DELETE A SCHEDULED EVENT\n")
    print("5) CLOSE SCHEDULE MANAGER \n(Note this will stop the tracking of all events it is recommended not to not close it\n but if you have to shut down your device select this option before you do so :)\n\n")
    try :
                choice=int(input("Enter Choice (a number from 1 to 5):"))
                if choice==1:
                    input1=inmod.Event()
                    input1.addevents()
                    input1.class_autocall()
                elif choice==2:
                    output1=outmod.Output()
                    output1.autoouput()
                elif choice==3:
                    update=outmod.Update()
                    update.Update_Details()
                elif choice==4:
                    delete=outmod.Update()
                    delete.Delete_Details()
                elif choice==5:
                    exit()
                else:
                    "INVALID INPUT!!!!!\n PLEASE CHOOSE AGAIN\n"
                    continue
                print("\n\n")
                input("PRESS ANY KEY TO CONTINUE")
                print("\n\n")
    except ValueError:
                print("\nINVALID INPUT\n\n")


#obj69=MAINCLASS()
#obj69.start()


