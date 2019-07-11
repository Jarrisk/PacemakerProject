#Hey/Hola/Bonjour/Jambo/etc to everyone at Children's Hospital!
 
#I hope you don't find this too confusing, and if you do, just reach out to me! 
#My personal email is jarriskeegan@gmail.com. If you find bugs/incorrect logic
#or simply confusing aspects about the program, I'll be more than happy to help when I am available.


#I advise reading all the comments in a linear fashion from start to finish, otherwise none of this will make sense.
#I also recommend going over what a "while" and "if" statement are. They're not mandatory to know, but, it'll make
#things a lot easier for you if you know what they are.

#----------------------------------------------------------------------------------------#

#Importing all the python libraries needed into the program. Please look at the readme document to find out how to download 
#these libraries. Some of these libraries dont need installed, per say, because they already come with python 3.7.
import csv
import serial
import numpy as np
from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
import pdb
import time


#This is the layout of the screen the user interacts with. The functions for both heartblock and junctional arrhythmias
#are called here.
class MainPage(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.init_window()
    def init_window(self):
        self.master.title("Select Arrythmia Scenario")
        self.pack(fill=BOTH,expand=1)
        Arrythmia1=Button(self,text="Heartblock",command=self.Heartblock)
        Arrythmia2=Button(self,text="Junctional",command=self.Junctional)
        Arrythmia1.place(x=0,y=0)
        Arrythmia2.place(x=100,y=0)



#Heartblock Function. I didn't add any comments to the Junctional function because it works the exact same way, just using a different dataset to show Junctional arrhythmia.
    def Heartblock(self):
        #initializing variables/arrays that are used
        x=[]
        y=[]
        yn=[]
        y0=[]
        s=[]
        insertdiff=[]
        plot_window = 50
        plot_increment= 50
        g_var = np.array(np.zeros([plot_window]))
        y_var = np.array(np.zeros([0]))
        x_var=np.array(np.zeros([plot_window]))
        plt.ion()
        fig1, ax1 = plt.subplots()
        line1, = ax1.plot(x_var,g_var,'--')
        line2, =ax1.plot(x,y)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('EKG (mV)')
        ax2=ax1.twinx()
        ax2.set_ylabel('Pacing pulse (Volts)')
        plt.title('EKG Signal with Pulse Plot')
        plt.yticks(np.arange(6),(0,.25,0.5,.75,1,1.25))
        plt.xticks(np.arange(6),(0,1.0,2.0,3.0,4.0,5.0))

        #Subfunction that opens data files for heartblock, time, and the ecg.
        def openfile():
            try:
                with open('heartblock.csv','r',encoding='utf-8') as ecgFile:
                    ecgData = csv.reader(ecgFile, delimiter=',')
                    for columns in ecgData:
                        y.append(columns)
                with open('heartblock.csv','r',encoding='utf-8') as ecgFile:
                    ecgData = csv.reader(ecgFile, delimiter=',')
                    for columns in ecgData:
                        y0.append(columns)
                with open('ecg.csv','r',encoding='utf-8') as ecgFile:
                    ecgData = csv.reader(ecgFile, delimiter=',')
                    for columns in ecgData:
                        yn.append(columns)
                with open ('serialvec.csv','r',encoding='utf-8') as serialvec:
                    timedata=csv.reader(serialvec, delimiter=',')
                    for columns in timedata:
                        x.append(columns)
            except ValueError:
                print ('No files found')
    
        #Initializing more variables
        index = np.array(np.zeros([1]))
        indexfinish = np.array(np.zeros([1]))
        timediff = np.array(np.zeros([1]))
        i=0
        j=0
        k=0
        prevtime=0
        currenttime=0
        openfile();  
        #This next part graphs the Heartblock ECG.
        #To decrease the speed of the ECG, modify the number inside "time.sleep".
        #A higher number inside "time.sleep" creates a slower ECG signal.
        #In order to keep the Heartblock ECG graph going, keep the power button off on the black box. 
        #Once the user thinks they have correctly set the pacemaker to the right settings, press the power button.
        while j==0:
            line2.set_data(x[:(i*26)],y[:(i*26)])
            line2.axes.axis([0, 5.3, -300, 300])    
            if i==52: 
                i=0
            else:
                i=i+1
            time.sleep(.05)
            plt.show()     
            fig1.canvas.flush_events()
            try:
                
                ser = serial.Serial('COM3',9600)
                ser_bytes = ser.readline()
                ser.flushInput()
                currenttime = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))    
                if currenttime>0.0:
                    plt.close()
                    j=1
            except:
                continue

        #This part reads in the times at which the pacemaker pulses.
        #Once two times are recorded, the difference between those times is calculated.
        # These time stamps were initially recorded as miliseconds. Therefore, by dividing by 100 (as seen the code),
        # insertdiff records these time stamps as tenths of a second.  
        j=0
        print('loading.')   
        while j<20:
            print('......')
            previoustime=currenttime
            ser_bytes = ser.readline()
            currenttime = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            insertdiff=(currenttime-previoustime)/100
            
            #VERY IMPORTANT: The number stored inside "insertdiff" is used to create an equal amount of zeroes.
            #for example: if insertdiff=7 (which would be .7 seconds), then seven zeroes will be put inside y_var.
            #At that point, a pulse will occur.

            
            y_var=np.append(y_var,np.zeros([insertdiff]))
            
            
            #Based on the command above, y_var=[0 0 0 0 0 0 0] (using the example of insertdiff=7)
            
            y_var=np.append(y_var,150)

            #Based on the command above, y_var=[0 0 0 0 0 0 0 150]

            j=j+1
        
        #reinitializing variables
        plt.ion()
        fig1, ax1 = plt.subplots()
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('EKG (mV)')
        ax2=ax1.twinx()
        ax2.set_ylabel('Pacing pulse (Volts)')
        x=[]
        y=[]
        line1, = ax1.plot(x_var,g_var,'--')
        line2, =ax1.plot(x,y)
        openfile(); 
        j=0
        
        while True:
                if i<51:
                    if i<50:
                        if g_var[i]>100:
                            index=np.append(index,i)
                            if len(index)>2:
                                if len(index)==3:
                                    j=j+2
                                else:
                                    j=j+1
                                #THIS IS THE MOST IMPORTANT PART FOR THE CLINICIANS
                                #Each time a pulse is found, "index" is appended with the "i" value where that pulse occures
                                #That "i" value corresponds to the tenths of seconds that have passed since a pulse occured
                                indexsub=index[j]-index[j-1]
                                
                                #If the time passed between pulses is appropriately set, it should fix the arrhythmia.
                                #That time is found within "np.float64". I've set the number "7", which corresponds to
                                #seven tenths of a second, as a correct value. When seven tenths of a second have passed,
                                #the terminal prints "correct", showing the user has changed the pacemaker to the correct 
                                # setting

                                #That being said, the clinicians will have to modify the value inside "np.float64"
                                #to allow the correct setting on the pacemaker to show "correct" on the terminal.
                                if indexsub==np.float64(7):
                                    indexfinish=np.append(indexfinish,indexsub)
                                    print('correct!')
                                    if(len(indexfinish))>5:
                                       y=yn 
                                else:
                                    print('incorrect')
                                    y=y0
                #This part moves the graphs of both the pulse and ECG plots.
                x_var=np.append(x_var,float(''.join(x[i*26])))
                x_var=x_var[1:plot_increment+1]
                g_var=y_var[i:plot_increment+i]
                fig1.canvas.draw()
                line1.set_data(x_var[:(i*26)],g_var[:(i*26)])
                line2.set_data(x[:(i*26)],y[:(i*26)])
                line2.axes.axis([0, 5.3, -300, 300])
                
                #This restarts the graph, making it go through a loop continuously.
                if i==52: 
                    i=0
                    j=0
                    k=0
                    g_var = np.array(np.zeros([plot_window]))
                    x_var= np.array(np.zeros([plot_window])) 
                    indexsub=0
                    index = np.array(np.zeros([1]))
                else:
                    i=i+1
                #Again, if you want to slow/speed up the graph, increase/decrease the value inside "time.sleep"
                #this would modify the speed of the graph after the pacemaker data is read in
                    time.sleep(.05)
                plt.show()     
                fig1.canvas.flush_events()

    def Junctional(self):
        x=[]
        y=[]
        yn=[]
        y0=[]
        s=[]
        insertdiff=[]
        plot_window = 50
        plot_increment= 50
        g_var = np.array(np.zeros([plot_window]))
        y_var = np.array(np.zeros([0]))
        print(y_var)
        x_var=np.array(np.zeros([plot_window]))
        plt.ion()
        fig1, ax1 = plt.subplots()
        line1, = ax1.plot(x_var,g_var,'--')
        line2, =ax1.plot(x,y)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('EKG (mV)')
        ax2=ax1.twinx()
        ax2.set_ylabel('Pacing pulse (Volts)')
        plt.title('EKG Signal (Green) with Pulse Plot (Blue)')
        plt.yticks(np.arange(6),(0,.25,0.5,.75,1,1.25))
        plt.xticks(np.arange(6),(0,1.0,2.0,3.0,4.0,5.0))
        def openfile():
            try:
                with open('Junc.csv','r',encoding='utf-8') as ecgFile:
                    ecgData = csv.reader(ecgFile, delimiter=',')
                    for columns in ecgData:
                        y.append(columns)
                with open('Junc.csv','r',encoding='utf-8') as ecgFile:
                    ecgData = csv.reader(ecgFile, delimiter=',')
                    for columns in ecgData:
                        y0.append(columns)
                with open('ecg.csv','r',encoding='utf-8') as ecgFile:
                    ecgData = csv.reader(ecgFile, delimiter=',')
                    for columns in ecgData:
                        yn.append(columns)
                with open ('serialvec.csv','r',encoding='utf-8') as serialvec:
                    timedata=csv.reader(serialvec, delimiter=',')
                    for columns in timedata:
                        x.append(columns)
            except ValueError:
                print('No Files Found')

        index = np.array(np.zeros([1]))
        indexfinish = np.array(np.zeros([1]))
        timediff = np.array(np.zeros([1]))
        i=0
        j=0
        k=0
        prevtime=0
        currenttime=0
        openfile();  
        while j==0:
            line2.set_data(x[:(i*26)],y[:(i*26)])
            line2.axes.axis([0, 5.3, -300, 300])    
            if i==52: 
                i=0
            else:
                i=i+1
            plt.show() 
            time.sleep(.05)    
            fig1.canvas.flush_events()
            try:
                ser = serial.Serial('COM3',9600)
                ser_bytes = ser.readline()
                ser.flushInput()
                currenttime = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))    
                
                if currenttime>0.0:
                    plt.close()
                    j=1
            except:
                continue

        j=0
        print('loading.')
        while j<20:
            print('......')
            previoustime=currenttime
            ser_bytes = ser.readline()
            currenttime = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            insertdiff=(currenttime-previoustime)/100
            y_var=np.append(y_var,np.zeros([insertdiff]))
            y_var=np.append(y_var,150)
            j=j+1
        plt.ion()
        fig1, ax1 = plt.subplots()
        ax2=ax1.twinx()
        ax2.set_ylabel('Pacing pulse (Volts)')        
        x=[]
        y=[]
        line1, = ax1.plot(x_var,g_var,'--')
        line2, =ax1.plot(x,y)
        openfile(); 
        j=0
        while True:
                #start 
                if i<51:
                    if i<50:
                        if g_var[i]>100:
                            index=np.append(index,i)
                            if len(index)>2:
                                if len(index)==3:
                                    j=j+2
                                else:
                                    j=j+1
                                indexsub=index[j]-index[j-1]
                                if indexsub==np.float64(7):
                                    indexfinish=np.append(indexfinish,indexsub)
                                    print('correct!')
                                    if(len(indexfinish))>5:
                                        y=yn 
                                else:
                                    print('incorrect')
                                    y=y0
                x_var=np.append(x_var,float(''.join(x[i*26])))
                x_var=x_var[1:plot_increment+1]
                g_var=y_var[i:plot_increment+i]
                fig1.canvas.draw()
                line1.set_data(x_var[:(i*26)],g_var[:(i*26)])
                line2.set_data(x[:(i*26)],y[:(i*26)])
                line2.axes.axis([0, 5.3, -300, 300])
                if i==52: 
                    i=0
                    j=0
                    k=0
                    g_var = np.array(np.zeros([plot_window]))
                    x_var= np.array(np.zeros([plot_window])) 
                    indexsub=0
                    index = np.array(np.zeros([1]))
                else:
                    i=i+1
                    time.sleep(.05)
                plt.show()     
                fig1.canvas.flush_events()
root=Tk()
app=MainPage(root)
root.geometry("400x300")
root.mainloop()