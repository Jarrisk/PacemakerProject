import csv
import serial
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pdb

x=[]
y=[]
s=[]

ser = serial.Serial('/dev/cu.usbmodem14201',9600)
ser.flushInput()

plot_window = 50
plot_increment=50
y_var = np.array(np.zeros([plot_window]))
x_var= np.array(np.zeros([plot_window]))
plt.ion()
fig1, ax1 = plt.subplots()
line1, = ax1.plot(y_var,x_var,'--')
line2, =ax1.plot(x,y)
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('EKG (mV)')
ax2=ax1.twinx()
ax2.set_ylabel('Pacing pulse (Volts)')
plt.title('EKG Signal (Green) with Pulse Plot (Blue)')
plt.yticks(np.arange(6),(0,.25,0.5,.75,1,1.25))
plt.xticks(np.arange(6),(0,1.0,2.0,3.0,4.0,5.0))
with open('ecg.csv','r') as ecgFile:
    ecgData = csv.reader(ecgFile, delimiter=',')
    for columns in ecgData:
        y.append(columns)
with open ('serialvec.csv','r') as serialvec:
    timedata=csv.reader(serialvec, delimiter=',')
    for columns in timedata:
        x.append(columns)

i=0
j=0
while True:
    try:
        ser_bytes = ser.readline()
        try:    
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            
        except:
            continue
        if decoded_bytes>500:
            decoded_bytes=150
        y_var = np.append(y_var,decoded_bytes)
        
        x_var=np.append(x_var,float(''.join(x[i*26])))
        y_var = y_var[1:plot_increment+1]
        x_var=x_var[1:plot_increment+1]
        print(x[i*26])
        
        
        #ax1.relim()
        #ax1.autoscale_view()
        fig1.canvas.draw()
        line1.set_data(x_var[:(i*26)],y_var[:(i*26)])
        line2.set_data(x[:(i*26)],y[:(i*26)])
        line2.axes.axis([0, 5.3, -300, 300])
            
        if i==52:    
            i=0
            y_var = np.array(np.zeros([plot_window]))
            x_var= np.array(np.zeros([plot_window]))         
        else:
             i=i+1
        plt.show()     
    #    pdb.set_trace()
        fig1.canvas.flush_events()
        
    except:
        break