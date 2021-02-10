
import multiprocessing
import Events_Module_Input as inmod
import Processing as process
import Events_Module_output as outmod
import time


print("*********************************ASIAN INTERNATIONAL PRIVATE SCHOOL RUWAIS********************************************")
print("*******************************************RUWAIS ABU DHABI***********************************************************")
print("\t\tWELCOME TO YOUR DAY PLANNER\n\t\tUSE THIS TO PLAN YOUR DAY EFFICIENTLY\n\t\tFOLLOW THE ON SCREEN PROMPTS\n\t\tENJOY\n")
print("\t\tPlease wait patiently as the initial setup may take up to 1 minute\n\t\tDO NOT CLOSE THE PROGRAM!!\n\n\n\n\n\n\n")





obj1 = inmod.Simultaneous()
obj1.selfrun()
obj2=process.Processing()
queue=multiprocessing.Queue()
queue.put(1)


def RunProcess(queue):
    while True:
        if queue.empty()==True:
            obj2.autorun()

        else: # throw away function to keep the process alive
            a=2+3

p1=multiprocessing.Process(target=RunProcess,args=(queue,),name="hello")
p1.start()

while True:
        queue.get()  #starts the processp1.start()
        input("PRESS ANY KEY TO CONTINUE")
        print("\n\n")
        print("CHOOSE ANY OF THE FOLLOWING:\n\n")
        print("1) SCHEDULE A NEW EVENT\n")
        print("2) DISPLAY SCHEDULED EVENTS\n")
        print("3) UPDATE SCHEDULED EVENTS\n")
        print("4) DELETE A SCHEDULED EVENT\n")
        print("5) CLOSE SCHEDULE MANAGER \n(Note this will stop the tracking of all events it is recommended not to not close it\n but if you have to shut down your device select this option before you do so :)\n\n")
        try :
                    choice=int(input("Enter Choice (a number from 1 to 5):"))
                    queue.put(1)  # stops the process

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
                        p1.terminate()
                        exit()
                    else:
                        "INVALID INPUT!!!!!\n PLEASE CHOOSE AGAIN\n"
                        continue
                    print("\n\n")

        except ValueError:
            queue.put(1)  # stops the process
            print("\nINVALID INPUT\n\n")


