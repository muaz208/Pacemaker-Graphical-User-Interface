from email import message
from statistics import mode
from symbol import parameters
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import os
from turtle import bgcolor, width
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import serial.tools.list_ports as ports
import struct
import time
global user_file_location
import numpy as np
import matplotlib.animation as animation 
import random


# user_file_location='C:/Users/ssamu/Desktop/3K04/3K04_Group8/DCM/UserInfo.txt'
# user_var_location = 'C:/Users/ssamu/Desktop/3K04/3K04_Group8/DCM/UserVars.txt'


user_file_location='C:/Users/muaz2/Desktop/McMaster Engineering/Comp Eng Year 3/SFWRENG 3K04/Project/Project Folder/3K04_Group8/DCM/UserInfo.txt'
user_var_location = 'C:/Users/muaz2/Desktop/McMaster Engineering/Comp Eng Year 3/SFWRENG 3K04/Project/Project Folder/3K04_Group8/DCM/UserVars.txt'


def change_state():
    global plot
    if plot == True:
        plot = False
    else:
        plot = True



def refresh():
    global plot, ECG_data_1, a, line, canvas, x1
    if plot == True:
        x1 = np.append(x1, x1[-1]+0.1)
        ECG_data_1 = np.append(ECG_data_1, random.randint(0,5))
        a.set_xlim(x1[-1]-10, x1[-1])
        line.set_data(x1,ECG_data_1)       
        canvas.draw()
        screen.after(10, refresh)
   
def gui_handler():
    change_state()
    refresh()

def get_ECG_data():
    global ECG_data
    Start = b'\x16'
    ECG_set = b'\x77'
    garbage=struct.pack("B",0)
    ECG_request=Start +ECG_set + struct.pack("B",0)+ struct.pack("B",Lower_Rate_Limit.get()) +struct.pack("B",Upper_Rate_Limit.get()) +struct.pack("d",Atrial_Amp.get()) +struct.pack("d",Atrial_Pulse_Width.get()) +struct.pack("d",Ventricular_Amp.get()) +struct.pack("d",Ventricular_Pulse_Width.get()) +struct.pack("d",float(Vrp.get())) +struct.pack("d",float(Arp.get())) +struct.pack("d",Ventricular_Sensitivity.get()) +struct.pack("d",Atrial_Sensitivity.get()) +struct.pack("B",Activity_Threshold.get()) +struct.pack("B",Maximum_Sensor_Rate.get()) +struct.pack("B",Reaction_Time.get()) +struct.pack("B",Response_Factor.get()) +struct.pack("B",Recovery_Time.get())
    
    with serial.Serial("COM5", 115200) as pacemaker:
        pacemaker.reset_output_buffer()
        pacemaker.reset_input_buffer()
        print("Opening COM 5 for ECG")
        ecg_bytes=pacemaker.write(ECG_request)
        print("Wrote ecg request and sent bytes: ",ecg_bytes)
        time.sleep(1)
        print("Slept")
        ECG_data = pacemaker.read(160)
        pacemaker.close()
        print("Got data")
    print(len(ECG_data))
    i=0
    for x in range(160):
        temp=round(struct.unpack("d",ECG_data[i:i+8])[0],1)
        print(temp*1000)
        i=i+8
        if((i+8)>160):
            break

    


def stop_ECG_data():
    pass

def DCM_to_Pacemaker():
    save_variables()


    Start = b'\x16'
    SYNC = b'\x22'
    Fn_set = b'\x55'
    garbage = struct.pack("B", 0)



    Pacemakermode=0
    if(selectedMode=="AOO"):
        Pacemakermode=0
    elif(selectedMode=="AAI"):
        Pacemakermode=2
    elif(selectedMode=="VOO"):
        Pacemakermode=1
    elif(selectedMode=="VVI"):
        Pacemakermode=3
    elif(selectedMode=="AOOR"):
        Pacemakermode=4
    elif(selectedMode=="VOOR"):
        Pacemakermode=5
    elif(selectedMode=="AAIR"):
        Pacemakermode=6
    elif(selectedMode=="VVIR"):
        Pacemakermode=7
    else:
        Pacemakermode=0


    print(Lower_Rate_Limit.get())
    print(Upper_Rate_Limit.get())




    PaceMakerParams = Start +Fn_set + struct.pack("B",Pacemakermode)+ struct.pack("B",Lower_Rate_Limit.get()) +struct.pack("B",Upper_Rate_Limit.get()) +struct.pack("d",Atrial_Amp.get()) +struct.pack("d",Atrial_Pulse_Width.get()) +struct.pack("d",Ventricular_Amp.get()) +struct.pack("d",Ventricular_Pulse_Width.get()) +struct.pack("d",float(Vrp.get())) +struct.pack("d",float(Arp.get())) +struct.pack("d",Ventricular_Sensitivity.get()) +struct.pack("d",Atrial_Sensitivity.get()) +struct.pack("B",Activity_Threshold.get()) +struct.pack("B",Maximum_Sensor_Rate.get()) +struct.pack("B",Reaction_Time.get()) +struct.pack("B",Response_Factor.get()) +struct.pack("B",Recovery_Time.get())
    GetFromPacemaker=Start +SYNC + struct.pack("B",Pacemakermode)+ struct.pack("B",Lower_Rate_Limit.get()) +struct.pack("B",Upper_Rate_Limit.get()) +struct.pack("d",Atrial_Amp.get()) +struct.pack("d",Atrial_Pulse_Width.get()) +struct.pack("d",Ventricular_Amp.get()) +struct.pack("d",Ventricular_Pulse_Width.get()) +struct.pack("d",Vrp.get()) +struct.pack("d",Arp.get()) +struct.pack("d",Ventricular_Sensitivity.get()) +struct.pack("d",Atrial_Sensitivity.get()) +struct.pack("B",Activity_Threshold.get()) +struct.pack("B",Maximum_Sensor_Rate.get()) +struct.pack("B",Reaction_Time.get()) +struct.pack("B",Response_Factor.get()) +struct.pack("B",Recovery_Time.get()) 

    with serial.Serial("COM5", 115200) as pacemaker:
        pacemaker.reset_output_buffer()
        pacemaker.reset_input_buffer()
        print("Opening COM 5 for sending params")
        bytes=pacemaker.write(PaceMakerParams)
        pacemaker.close()
        print("closed COM5 and sent number of bytes: ",bytes)

    time.sleep(2)
    
    with serial.Serial("COM5", 115200,timeout=2) as pacemaker:
        pacemaker.reset_output_buffer()
        pacemaker.reset_input_buffer()
        print("Opening COM 5 for echo")
        echo_bytes=pacemaker.write(GetFromPacemaker)
        print("Wrote echo and sent bytes: ",echo_bytes)
        time.sleep(1)
        print("Slept")
        x = pacemaker.read(74)
        pacemaker.close()
        print("Closing COM5")


    try:
        PMMode= x[0]
        LRL = x[1]
        URL = x[2]
        Pacemaker_Atrial_AMP= round(struct.unpack("d",x[3:11])[0],1)
        Pacemaker_Atrial_PW = round(struct.unpack("d",x[11:19])[0],1)
        Pacemaker_V_AMP= round(struct.unpack("d",x[19:27])[0],1)
        Pacemaker_V_PW = round(struct.unpack("d",x[27:35])[0],1)
        Pacemaker_vrp=round(struct.unpack("d",x[35:43])[0],1)
        Pacemaker_arp=round(struct.unpack("d",x[43:51])[0],1)
        Pacemaker_Ventricular_Sensitivity=round(struct.unpack("d",x[51:59])[0],1)
        Pacemaker_Atrial_Sensitivity=round(struct.unpack("d",x[59:67])[0],1)
        Pacemaker_activity_threshold=x[67]
        Pacemaker_max_sensor_rate=x[68]
        Pacemaker_reaction_time=x[69]
        Pacemaker_response_factor=x[70]
        Pacemaker_recovery_time=x[71]

        print(PMMode,LRL,URL,Pacemaker_Atrial_AMP,Pacemaker_Atrial_PW,Pacemaker_V_AMP,Pacemaker_V_PW,Pacemaker_vrp,Pacemaker_arp,Pacemaker_Ventricular_Sensitivity,Pacemaker_Atrial_Sensitivity)
        print(Pacemaker_activity_threshold,Pacemaker_max_sensor_rate,Pacemaker_reaction_time,Pacemaker_response_factor,Pacemaker_recovery_time)
    except:
        print("Error")
        return

    


def modeSelection(selection):
    global selectedMode
    selectedMode=selection

    Ventricular_Amp_dislpay.config(state='disabled')
    Ventricular_Pulse_Width_display.config(state='disabled')
    Vrp_display.config(state='disabled')
    Atrial_Amp_display.config(state='normal')
    Atrial_Pulse_Width_display.config(state='normal')
    Arp_dispay.config(state='disabled')
    Atrial_Sensitivity_display.config(state='disabled')
    Ventricular_Sensitivity_display.config(state='disabled')
    Maximum_Sensor_Rate_display.config(state='disabled')
    Activity_Threshold_display.config(state='disabled')
    Reaction_Time_display.config(state='disabled')
    Response_Factor_display.config(state='disabled')
    Recovery_Time_display.config(state='disabled')
    
    if(selection=="AOO" ):
        Ventricular_Amp_dislpay.config(state='disabled')
        Ventricular_Pulse_Width_display.config(state='disabled')
        Vrp_display.config(state='disabled')
        Atrial_Amp_display.config(state='normal')
        Atrial_Pulse_Width_display.config(state='normal')
        Arp_dispay.config(state='disabled')
        Atrial_Sensitivity_display.config(state='disabled')
        Ventricular_Sensitivity_display.config(state='disabled')
        Maximum_Sensor_Rate_display.config(state='disabled')
        Activity_Threshold_display.config(state='disabled')
        Reaction_Time_display.config(state='disabled')
        Response_Factor_display.config(state='disabled')
        Recovery_Time_display.config(state='disabled')
    elif(selection=="AAI"):
        Ventricular_Amp_dislpay.config(state='disabled')
        Ventricular_Pulse_Width_display.config(state='disabled')
        Vrp_display.config(state='disabled')
        Atrial_Amp_display.config(state='normal')
        Atrial_Pulse_Width_display.config(state='normal')
        Arp_dispay.config(state='normal')
        Atrial_Sensitivity_display.config(state='normal')
        Ventricular_Sensitivity_display.config(state='disabled')
        Maximum_Sensor_Rate_display.config(state='disabled')
        Activity_Threshold_display.config(state='disabled')
        Reaction_Time_display.config(state='disabled')
        Response_Factor_display.config(state='disabled')
        Recovery_Time_display.config(state='disabled')
    elif(selection=="VVI"):
        Ventricular_Amp_dislpay.config(state='normal')
        Ventricular_Pulse_Width_display.config(state='normal')
        Vrp_display.config(state='normal')
        Atrial_Amp_display.config(state='disabled')
        Atrial_Pulse_Width_display.config(state='disabled')
        Arp_dispay.config(state='disabled')
        Atrial_Sensitivity_display.config(state='disabled')
        Ventricular_Sensitivity_display.config(state='normal')
        Maximum_Sensor_Rate_display.config(state='disabled')
        Activity_Threshold_display.config(state='disabled')
        Reaction_Time_display.config(state='disabled')
        Response_Factor_display.config(state='disabled')
        Recovery_Time_display.config(state='disabled')


    elif(selection=="VOO"):
        Ventricular_Amp_dislpay.config(state='normal')
        Ventricular_Pulse_Width_display.config(state='normal')
        Vrp_display.config(state='disabled')
        Atrial_Amp_display.config(state='disabled')
        Atrial_Pulse_Width_display.config(state='disabled')
        Arp_dispay.config(state='disabled')
        Atrial_Sensitivity_display.config(state='disabled')
        Ventricular_Sensitivity_display.config(state='disabled')
        Maximum_Sensor_Rate_display.config(state='disabled')
        Activity_Threshold_display.config(state='disabled')
        Reaction_Time_display.config(state='disabled')
        Response_Factor_display.config(state='disabled')
        Recovery_Time_display.config(state='disabled')

    elif(selection=="AOOR"):
        Ventricular_Amp_dislpay.config(state='disabled')
        Ventricular_Pulse_Width_display.config(state='disabled')
        Vrp_display.config(state='disabled')
        Atrial_Amp_display.config(state='normal')
        Atrial_Pulse_Width_display.config(state='normal')
        Arp_dispay.config(state='disabled')
        Atrial_Sensitivity_display.config(state='disabled')
        Ventricular_Sensitivity_display.config(state='disabled')
        Maximum_Sensor_Rate_display.config(state='normal')
        Activity_Threshold_display.config(state='normal')
        Reaction_Time_display.config(state='normal')
        Response_Factor_display.config(state='normal')
        Recovery_Time_display.config(state='normal')
    
    elif(selection=="VOOR"):
        Ventricular_Amp_dislpay.config(state='normal')
        Ventricular_Pulse_Width_display.config(state='normal')
        Vrp_display.config(state='disabled')
        Atrial_Amp_display.config(state='disabled')
        Atrial_Pulse_Width_display.config(state='disabled')
        Arp_dispay.config(state='disabled')
        Atrial_Sensitivity_display.config(state='disabled')
        Ventricular_Sensitivity_display.config(state='disabled')
        Maximum_Sensor_Rate_display.config(state='normal')
        Activity_Threshold_display.config(state='normal')
        Reaction_Time_display.config(state='normal')
        Response_Factor_display.config(state='normal')
        Recovery_Time_display.config(state='normal')

    elif(selection=="AAIR"):
        Ventricular_Pulse_Width_display.config(state='disabled')
        Vrp_display.config(state='disabled')
        Atrial_Amp_display.config(state='normal')
        Atrial_Pulse_Width_display.config(state='normal')
        Arp_dispay.config(state='normal')
        Atrial_Sensitivity_display.config(state='normal')
        Ventricular_Sensitivity_display.config(state='disabled')
        Maximum_Sensor_Rate_display.config(state='normal')
        Activity_Threshold_display.config(state='normal')
        Reaction_Time_display.config(state='normal')
        Response_Factor_display.config(state='normal')
        Recovery_Time_display.config(state='normal')
    elif(selection=="VVIR"):
        Ventricular_Amp_dislpay.config(state='normal')
        Ventricular_Pulse_Width_display.config(state='normal')
        Vrp_display.config(state='normal')
        Atrial_Amp_display.config(state='disabled')
        Atrial_Pulse_Width_display.config(state='disabled')
        Arp_dispay.config(state='disabled')
        Atrial_Sensitivity_display.config(state='disabled')
        Ventricular_Sensitivity_display.config(state='normal')
        Maximum_Sensor_Rate_display.config(state='normal')
        Activity_Threshold_display.config(state='normal')
        Reaction_Time_display.config(state='normal')
        Response_Factor_display.config(state='normal')
        Recovery_Time_display.config(state='normal')
    else:
        Ventricular_Amp_dislpay.config(state='normal')
        Ventricular_Pulse_Width_display.config(state='normal')
        Vrp_display.config(state='normal')
        Atrial_Amp_display.config(state='normal')
        Atrial_Pulse_Width_display.config(state='normal')
        Arp_dispay.config(state='normal')
        Atrial_Sensitivity_display.config(state='normal')
        Ventricular_Sensitivity_display.config(state='normal')
        Maximum_Sensor_Rate_display.config(state='normal')
        Activity_Threshold_display.config(state='normal')
        Reaction_Time_display.config(state='normal')
        Response_Factor_display.config(state='normal')
        Recovery_Time_display.config(state='normal')

    



    
    return

def variable_upload():
     # read the previous variable values if there are any, upon login
    is_in = 0
    with open(user_var_location,'r') as UserVals:
        lines = UserVals.readlines()
    for line in lines:
        username_and_vars= line.strip().split(',')
        if (username1 == username_and_vars[0]):
            is_in = 1
            break
    UserVals.close()

    if is_in == 1:
        Lower_Rate_Limit_display.delete(0, "end")
        Upper_Rate_Limit_display.delete(0, "end")
        Atrial_Amp_display.delete(0, "end")
        Atrial_Pulse_Width_display.delete(0, "end")
        Ventricular_Amp_dislpay.delete(0, "end")
        Ventricular_Pulse_Width_display.delete(0, "end")
        Vrp_display.delete(0, "end")
        Arp_dispay.delete(0, "end")
        Atrial_Sensitivity_display.delete(0, "end")
        Ventricular_Sensitivity_display.delete(0, "end")
        Maximum_Sensor_Rate_display.delete(0, "end")
        Activity_Threshold_display.delete(0, "end")
        Reaction_Time_display.delete(0, "end")
        Response_Factor_display.delete(0, "end")
        Recovery_Time_display.delete(0, "end")

        Mode.set(username_and_vars[1])
        Lower_Rate_Limit_display.insert(-1, username_and_vars[2])
        Upper_Rate_Limit_display.insert(-1, username_and_vars[3])
        Atrial_Amp_display.insert(-1, username_and_vars[4])
        Atrial_Pulse_Width_display.insert(-1, username_and_vars[5])
        Ventricular_Amp_dislpay.insert(-1, username_and_vars[6])
        Ventricular_Pulse_Width_display.insert(-1, username_and_vars[7])
        Vrp_display.insert(-1, username_and_vars[8])
        Arp_dispay.insert(-1, username_and_vars[9])
        Atrial_Sensitivity_display.insert(-1, username_and_vars[10])
        Ventricular_Sensitivity_display.insert(-1, username_and_vars[11])
        Maximum_Sensor_Rate_display.insert(-1, username_and_vars[12])
        Activity_Threshold_display.insert(-1, username_and_vars[13])
        Reaction_Time_display.insert(-1, username_and_vars[14])
        Response_Factor_display.insert(-1, username_and_vars[15])
        Recovery_Time_display.insert(-1, username_and_vars[16])
        modeSelection(username_and_vars[1])
        vis = Label(ParametersTab,text="Previous user inputs uploaded",fg="green",font=("calibri",11))
        vis.place(x=425,y=500)
        vis.after(3000, lambda: vis.destroy())
    else:
        vis = Label(ParametersTab,text="No previous user data to upload",fg="red",font=("calibri",11))
        vis.place(x=415,y=500)
        vis.after(3000, lambda: vis.destroy())
        modeSelection("AOO")

   
    

def reset_variables():
    Lower_Rate_Limit_display.delete(0, "end")
    Upper_Rate_Limit_display.delete(0, "end")
    Atrial_Amp_display.delete(0, "end")
    Atrial_Pulse_Width_display.delete(0, "end")
    Ventricular_Amp_dislpay.delete(0, "end")
    Ventricular_Pulse_Width_display.delete(0, "end")
    Vrp_display.delete(0, "end")
    Arp_dispay.delete(0, "end")
    Atrial_Sensitivity_display.delete(0, "end")
    Ventricular_Sensitivity_display.delete(0, "end")
    Maximum_Sensor_Rate_display.delete(0, "end")
    Activity_Threshold_display.delete(0, "end")
    Reaction_Time_display.delete(0, "end")
    Response_Factor_display.delete(0, "end")
    Recovery_Time_display.delete(0, "end")

    
    Lower_Rate_Limit_display.insert(-1, 0)
    Upper_Rate_Limit_display.insert(-1, 0)
    Atrial_Amp_display.insert(-1, 0)
    Atrial_Pulse_Width_display.insert(-1, 0)
    Ventricular_Amp_dislpay.insert(-1, 0)
    Ventricular_Pulse_Width_display.insert(-1, 0)
    Vrp_display.insert(-1, 0)
    Arp_dispay.insert(-1, 0)
    Atrial_Sensitivity_display.insert(-1, 0)
    Ventricular_Sensitivity_display.insert(-1, 0)
    Maximum_Sensor_Rate_display.insert(-1, 0)
    Activity_Threshold_display.insert(-1, 0)
    Reaction_Time_display.insert(-1, 0)
    Response_Factor_display.insert(-1, 0)
    Recovery_Time_display.insert(-1, 0)
    vis = Label(ParametersTab,text="On screen variable reset completed",fg="green",font=("calibri",11))
    vis.place(x=450,y=500)
    vis.after(3000, lambda: vis.destroy())
   
def save_variables():
 #Store the users User name and password in a text file
    cwd = os.getcwd()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    is_in = 0
    current_user_index = 0
    count_lines = 0
    #Check to ensure parameters are in valid range
    #Lower Rate Limit Check
    if((Lower_Rate_Limit.get()>=30 and Lower_Rate_Limit.get()<=50 ) or (Lower_Rate_Limit.get()>=90 and Lower_Rate_Limit.get()<=175 )):
        if(Lower_Rate_Limit.get()%5==0):
            pass
        else:
            messagebox.showerror('Warning','Lower Rate Limit Must be in the Valid Range')
            return
    elif(Lower_Rate_Limit.get()>=50 and Lower_Rate_Limit.get()<=90 ):
        pass
    else:
        messagebox.showerror('Warning','Lower Rate Limit Must be in the Valid Range')
        return

    #Upper Rate Limit Check
    if(Upper_Rate_Limit.get()>=50 and Upper_Rate_Limit.get()<=175 ):
        if(Upper_Rate_Limit.get()%5==0):
            pass
        else:
            messagebox.showerror('Warning','Upper Rate Limit Must be in the Valid Range')
            return
    else:
        messagebox.showerror('Warning','Upper Rate Limit Must be in the Valid Range')
        return


    #Atrial Amp Limit Check
    if(Atrial_Amp.get()>=float(0.1) and Atrial_Amp.get()<=float(5.0)):
        if(Atrial_Amp.get()%0.1<1):
            pass
        else:
            messagebox.showerror('Warning','Atrial Pulse Amplitude Must be in the Valid Range')
            return
    else:
            messagebox.showerror('Warning','Atrial Pulse Amplitude Must be in the Valid Range')
            return

    #Ventrical Amp Limit Check
    if(Ventricular_Amp.get()>=float(0.1) and Ventricular_Amp.get()<=float(5.0)):
        if(Ventricular_Amp.get()%0.1<1):
            pass
        else:
            messagebox.showerror('Warning','Ventricular Pulse Amplitude Must be in the Valid Range')
            return
    else:
            messagebox.showerror('Warning','Ventricular Pulse Amplitude Must be in the Valid Range')
            return



    #Atrial Pulse Width check
    if(Atrial_Pulse_Width.get()>=int(1) and Atrial_Pulse_Width.get()<=int(30)):
        if(Atrial_Pulse_Width.get()%1==0):
            pass
        else:
            messagebox.showerror('Warning','Atrial Pulse Width Must be in the Valid Range')
            return
    else:
        messagebox.showerror('Warning','Atrial Pulse Width Must be in the Valid Range')
        return



    #Ventrical Pulse Width check
    if(Ventricular_Pulse_Width.get()>=int(1) and Ventricular_Pulse_Width.get()<=int(30)):
        if(Ventricular_Pulse_Width.get()%1==0):
            pass
        else:
            messagebox.showerror('Warning','Ventrical Pulse Width Must be in the Valid Range')
            return
    else:
        messagebox.showerror('Warning','Ventrical Pulse Width Must be in the Valid Range')
        return


    #ARP Bound check
    if(Arp.get()>=150 and Arp.get()<=500):
        if(Arp.get()%10==0):
            pass
        else:
            messagebox.showerror('Warning','ARP Must be in the Valid Range')
            return
    else:
            messagebox.showerror('Warning','ARP Must be in the Valid Range')
            return

    #VRP Bound check
    if(Vrp.get()>=150 and Vrp.get()<=500):
        if(Vrp.get()%10==0):
            pass
        else:
            messagebox.showerror('Warning','VRP Must be in the Valid Range')
            return
    else:
            messagebox.showerror('Warning','VRP Must be in the Valid Range')
            return

    if(Lower_Rate_Limit.get() > Upper_Rate_Limit.get()):
        messagebox.showerror('Warning','Lower Rate Limit must not exceed Upper Rate Limit')
        return


    # see if username data has already been created, this can be implemented much better with less lines, do this for Assignment #2
    with open(user_var_location,'r') as fileinfo:
        for line in fileinfo:
            username_and_vars= line.strip().split(',')
            if (username_and_vars[0] == username1):
                is_in = 1
                current_user_index = count_lines
            count_lines += 1

    if is_in == 0:
        UserVals=open(user_var_location,'a')
        UserVals.write(username1 + "," + str(selectedMode)+","+ str(Lower_Rate_Limit.get()) + "," + str(Upper_Rate_Limit.get()) + "," + str(round(Atrial_Amp.get(),1)) + ',' +  str(round(Atrial_Pulse_Width.get(),1)) + ',' + str(round(Ventricular_Amp.get(),1)) + ',' +  str(round(Ventricular_Pulse_Width.get(),1)) + ',' + str(Vrp.get()) + ',' + str(Arp.get()) + ','+ str(Atrial_Sensitivity.get()) +',' + str(Ventricular_Sensitivity.get()) +','+ str(Maximum_Sensor_Rate.get())+ ','+ str(Activity_Threshold.get()) + ',' + str(Reaction_Time.get()) + ',' + str(Response_Factor.get()) + ',' + str(Recovery_Time.get()) + '\n')
        UserVals.close()
        save_done = 1

    else:
        with open(user_var_location,'r') as UserVals:
            lines = UserVals.readlines()

        try:  
            lines[current_user_index] = username1 + "," +str(selectedMode)+","+ str(Lower_Rate_Limit.get()) + "," + str(Upper_Rate_Limit.get()) + "," + str(round(Atrial_Amp.get(),1)) + ',' +  str(round(Atrial_Pulse_Width.get(),1)) + ',' + str(round(Ventricular_Amp.get(),1)) + ',' +  str(round(Ventricular_Pulse_Width.get(),1)) + ',' + str(Vrp.get()) + ',' + str(Arp.get()) + ','+ str(Atrial_Sensitivity.get()) +',' + str(Ventricular_Sensitivity.get()) +','+ str(Maximum_Sensor_Rate.get())+ ','+ str(Activity_Threshold.get()) + ',' + str(Reaction_Time.get()) + ',' + str(Response_Factor.get()) + ',' + str(Recovery_Time.get()) + '\n'
            vis = Label(ParametersTab,text="User variable save completed",fg="green",font=("calibri",11))
            vis.place(x=450,y=500)
            vis.after(3000, lambda: vis.destroy())
        except:
            vis = Label(ParametersTab,text="Ensure that all inputed variables are integer values",fg="red",font=("calibri",11))
            vis.place(x=400,y=500)
            vis.after(1500, lambda: vis.destroy())
        with open(user_var_location,'w') as UserVals:
            UserVals.writelines(lines)
    




      

def login_session():
    #screen.withdraw()
    screen2.destroy()
    UserSession=Toplevel(screen)
    UserSession.title("User Session")
    UserSession.geometry("1080x1920")

    global ParametersTab
    tabs=ttk.Notebook(UserSession)
    ParametersTab=ttk.Frame(tabs)
    ConnectiviteyTab=ttk.Frame(tabs)
    ECGTab=ttk.Frame(tabs)
    tabs.add(ParametersTab,text="Programable Parameters")
    tabs.add(ConnectiviteyTab,text="Connectivity")
    tabs.add(ECGTab,text="ECG")
    tabs.pack(expand=1,fill="both")

    # Parameters
    ModesOfOperation=["AOO","VOO","AAI","VVI","AOOR","VOOR","AAIR","VVIR"]
    global Mode
    global dropdown_mode_option
    global Lower_Rate_Limit, Upper_Rate_Limit, Atrial_Amp, Atrial_Pulse_Width, Ventricular_Amp, Ventricular_Pulse_Width ,Vrp, Arp, Atrial_Sensitivity, Ventricular_Sensitivity,Maximum_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time
    global Lower_Rate_Limit_display, Upper_Rate_Limit_display, Atrial_Amp_display, Atrial_Pulse_Width_display, Ventricular_Amp_dislpay, Ventricular_Pulse_Width_display,Vrp_display, Arp_dispay, Atrial_Sensitivity_display, Ventricular_Sensitivity_display, Maximum_Sensor_Rate_display,Activity_Threshold_display, Reaction_Time_display, Response_Factor_display, Recovery_Time_display 

    Lower_Rate_Limit = IntVar()
    Upper_Rate_Limit = IntVar()
    Atrial_Amp = DoubleVar()
    Atrial_Pulse_Width = DoubleVar()
    Ventricular_Amp = DoubleVar()
    Ventricular_Pulse_Width = DoubleVar()
    Vrp = IntVar()
    Arp = IntVar()
    Atrial_Sensitivity = DoubleVar()
    Ventricular_Sensitivity=DoubleVar()
    Maximum_Sensor_Rate=IntVar()
    Activity_Threshold = IntVar()
    Reaction_Time = IntVar()
    Response_Factor = IntVar()
    Recovery_Time = IntVar()

    

    Mode=StringVar(ParametersTab)
    Label(ParametersTab,text="Operation Mode:",fg="black",font=("calibri",11)).place(x=0,y=10)
    dropdown_mode_option=ttk.OptionMenu(ParametersTab,Mode,ModesOfOperation[0],*ModesOfOperation,command=modeSelection)
    dropdown_mode_option.place(x=150,y=10)
    dropdown_mode_option.config(width=30)
    
    Label(ParametersTab,text="Lower Rate Limit (pulse/min)",fg="black",font=("calibri",11)).place(x=0,y=40)
    Lower_Rate_Limit_display=Spinbox(ParametersTab,from_=30,to=175,increment=5,textvariable=Lower_Rate_Limit,wrap=True)
    Lower_Rate_Limit_display.place(x=190,y=40)
    
    Label(ParametersTab,text="Upper Rate Limit (pulse/min)",fg="black",font=("calibri",11)).place(x=0,y=80)
    Upper_Rate_Limit_display=Spinbox(ParametersTab,from_=50,to=175,increment=5,textvariable=Upper_Rate_Limit,wrap=True)
    Upper_Rate_Limit_display.place(x=190,y=80)

    Label(ParametersTab,text="Atrial Amplitude (V)",fg="black",font=("calibri",11)).place(x=0,y=120)
    Atrial_Amp_display=Spinbox(ParametersTab,from_=0.1,to=5.0,increment=0.1,textvariable=Atrial_Amp,wrap=True)
    Atrial_Amp_display.place(x=190,y=120)

    Label(ParametersTab,text="Atrial Pulse Width (ms)",fg="black",font=("calibri",11)).place(x=0,y=160)
    Atrial_Pulse_Width_display=Spinbox(ParametersTab,from_=1,to=30,increment=1,textvariable=Atrial_Pulse_Width,wrap=True)
    Atrial_Pulse_Width_display.place(x=190,y=160)

    Label(ParametersTab,text="Ventricular Amplitude (V)",fg="black",font=("calibri",11)).place(x=0,y=200)
    Ventricular_Amp_dislpay=Spinbox(ParametersTab,from_=0.1,to=5.0,increment=0.1,textvariable=Ventricular_Amp,wrap=True)
    Ventricular_Amp_dislpay.place(x=190,y=200)

    Label(ParametersTab,text="Ventricular Pulse Width (ms)",fg="black",font=("calibri",11)).place(x=0,y=240)
    Ventricular_Pulse_Width_display=Spinbox(ParametersTab,from_=1,to=30,increment=1,textvariable=Ventricular_Pulse_Width,wrap=True)
    Ventricular_Pulse_Width_display.place(x=190,y=240)

    Label(ParametersTab,text="VRP (ms)",fg="black",font=("calibri",11)).place(x=0,y=280)
    Vrp_display=Spinbox(ParametersTab,from_=150,to=500,increment=10,textvariable=Vrp,wrap=True)
    Vrp_display.place(x=190,y=280)
    
    Label(ParametersTab,text="ARP (s)",fg="black",font=("calibri",11)).place(x=0,y=320)
    Arp_dispay=Spinbox(ParametersTab,from_=150,to=500,increment=10,textvariable=Arp,wrap=True)
    Arp_dispay.place(x=190,y=320)

    Label(ParametersTab,text="Atrial Sensitivity (mV)",fg="black",font=("calibri",11)).place(x=0,y=360)
    Atrial_Sensitivity_display=Spinbox(ParametersTab,from_=0.0,to=5.0,increment=0.1,textvariable=Atrial_Sensitivity,wrap=True)
    Atrial_Sensitivity_display.place(x=190,y=360)

    Label(ParametersTab,text="Ventricular Sensitivity (mV)",fg="black",font=("calibri",11)).place(x=0,y=400)
    Ventricular_Sensitivity_display=Spinbox(ParametersTab,from_=0.0,to=5.0,increment=0.1,textvariable=Ventricular_Sensitivity,wrap=True)
    Ventricular_Sensitivity_display.place(x=190,y=400)

    Label(ParametersTab,text="Maximum Sensor Rate (ppm)",fg="black",font=("calibri",11)).place(x=400,y=40)
    Maximum_Sensor_Rate_display=Spinbox(ParametersTab,from_=50,to=175,increment=5,textvariable=Maximum_Sensor_Rate,wrap=True)
    Maximum_Sensor_Rate_display.place(x=600,y=40)

    Label(ParametersTab,text="Activity Threshold (Level)",fg="black",font=("calibri",11)).place(x=400,y=80)
    Activity_Threshold_display=Spinbox(ParametersTab,from_=8,to=56,increment=8,textvariable=Activity_Threshold,wrap=True)
    Activity_Threshold_display.place(x=600,y=80)

    Label(ParametersTab,text="Reaction Time (sec)",fg="black",font=("calibri",11)).place(x=400,y=120)
    Reaction_Time_display=Spinbox(ParametersTab,from_=10,to=50,increment=10,textvariable=Reaction_Time,wrap=True)
    Reaction_Time_display.place(x=600,y=120)

    Label(ParametersTab,text="Response Factor",fg="black",font=("calibri",11)).place(x=400,y=160)
    Response_Factor_display=Spinbox(ParametersTab,from_=1,to=16,increment=1,textvariable=Response_Factor,wrap=True)
    Response_Factor_display.place(x=600,y=160)

    Label(ParametersTab,text="Recovery Time (min)",fg="black",font=("calibri",11)).place(x=400,y=200)
    Recovery_Time_display=Spinbox(ParametersTab,from_=2,to=16,increment=1,textvariable=Recovery_Time,wrap=True)
    Recovery_Time_display.place(x=600,y=200)




    variable_upload()

    # Store User data in text file
    Button(ParametersTab,text="Save", width=10,height=1, command=save_variables).place(x=550,y=450)
    Button(ParametersTab,text="Reset", width=10,height=1, command=reset_variables).place(x=450,y=450)
    Button(ParametersTab,text="Upload", width=10,height=1, command=DCM_to_Pacemaker).place(x=350,y=450)

    #select_clear()
    #username_verify.get()

    # Conectivity
    Label(ConnectiviteyTab,text="Conection Status: Connected",fg="black",font=("calibri",11)).place(x=0,y=10)
    Button(ECGTab,text="Start", width=10,height=1, command=get_ECG_data).place(x=450,y=450)
    Button(ECGTab,text="Stop", width=10,height=1, command=stop_ECG_data).place(x=550,y=450)


    logoutParamTab=Button(ParametersTab,text="Logout",height="2",width="10",command=lambda:[screen.deiconify(),UserSession.destroy()])
    logoutConnectivityTab=Button(ConnectiviteyTab,text="Logout",height="2",width="10",command=lambda:[screen.deiconify(),UserSession.destroy()])
    logoutParamTab.place(x=980,y=5)
    logoutConnectivityTab.place(x=980,y=5)


    # ECG Tab
    global plot, ECG_data_1, a, line, canvas, x1
    plot = False
    ECG_data_1 = [1,2,3,4,5]
    x1 = []
    length = len(ECG_data_1)
    for i in range(length):
        x1 = np.append(x1,i)
    fig = plt.Figure(figsize=(8,3),dpi =100)
    a = fig.add_subplot(111)

    line, = a.plot(x1,ECG_data_1,color='blue')
    fig.subplots_adjust(bottom=0.19)
    canvas = FigureCanvasTkAgg(fig, master=ECGTab)
    canvas.get_tk_widget().place(x=100,y=0)

    a.set_title ("Ventrical", fontsize=11) 
    a.set_ylabel("Y", fontsize=11)
    a.set_xlabel("X", fontsize=11)

    canvas.draw()
   
    Button(ECGTab,text="ECG", width=10,height=1, command=gui_handler).place(x=650,y=650)

    




def register_user():
    username_info=username.get()
    password_info=password.get()
    

    #Store the users User name and password in a text file
    cwd = os.getcwd()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    usernames_check=[]



    with open(user_file_location,'r') as fileinfo:
        for line in fileinfo:
            username_and_password = line.strip().split(',')
            usernames_check.append(username_and_password[0])

    x=len(usernames_check)

    if x>=10:
        Label(screen1,text="Could not Register, too many users",fg="red",font=("calibri",11)).pack()

    elif (len(username_info)==0):
        messagebox.showerror('Warning','Must Enter a User Name')


    elif (username_info in usernames_check):
        Label(screen1,text="User already exists",fg="red",font=("calibri",11)).pack()
        messagebox.showerror('Warning','This User Name Already Exists')
    
    elif ((" " in username_info) == True or (" " in password_info) == True ):
        Label(screen1,text="Invalid Entry",fg="red",font=("calibri",11)).pack()
        messagebox.showerror('Warning','Username or Password cannot have a space')

    else:
        Userfile=open(user_file_location,'a')
        Userfile.write(username_info +",")
        Userfile.write(password_info+"\n")
        Userfile.close()
        Label(screen1,text="Registration was succesfull",fg="green",font=("calibri",11)).pack()



    username_entry.delete(0, END)
    password_entry.delete(0, END)
    



def register(): #This is the register buttons function
    global screen1
    screen1=Toplevel(screen)
    screen1.title("Register Page")
    screen1.geometry("1080x1920")

    global username
    global password
    global username_entry
    global password_entry

    username= StringVar()
    password=StringVar()
    Label(screen1,text="Please fill out the form below").pack()
    Label(screen1,text="").pack()

    Label(screen1,text="Username *").pack()
    username_entry=Entry(screen1,textvariable=username)
    username_entry.pack()
    Label(screen1,text="Password *").pack()
    password_entry=Entry(screen1,show="*",textvariable=password)
    password_entry.pack()
    Button(screen1,text="Register", width=10,height=1, command=register_user).pack()
    Label(screen1,text="").pack()
    Label(screen1,text="").pack()
    Button(screen1,text="Return to Login", width=12,height=1, command=screen1.destroy).pack()

    
def login_verify():
    global username1
    username1=username_verify.get()
    password1=password_verify.get()

    username_list=[]
    password_list=[]


    username_entry1.delete(0, END)
    password_entry1.delete(0, END)
    with open(user_file_location,'r') as fileinfo:
        for line in fileinfo:
            username_and_password = line.strip().split(',')
            username_list.append(username_and_password[0])
            password_list.append(username_and_password[1])
    if (len(username1)==0):
        messagebox.showerror('Warning','Enter a Username')   
    elif username1 in username_list: #Check to see if user exists in the username list
        if password1 == password_list[username_list.index(username1)]: #if the user exists, check to see if the entered password matches with the password for that user at its respective index in password list
            Label(screen2,text="Login was Succesfull",fg="green",font=("calibri",11)).place(x=500,y=1000)
            #New function called login_success will go here
            login_session()
        else:
            Label(screen2,text="Incorrect Password",fg="red",font=("calibri",11)).pack()
            messagebox.showerror('Error','Username or Password is Incorrect')
    else:
        Label(screen2,text="User not Found",fg="red",font=("calibri",11)).pack()



def login():  
    global screen2
    screen2=Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("1080x1920")

    Label(screen2,text="Please login below").pack()
    Label(screen2,text="").pack()

    global username_verify
    global password_verify #User name and password that user enters to login

    global username_entry1
    global password_entry1
    username_verify=StringVar()
    password_verify=StringVar()

    Label(screen2,text="Username").pack()
    username_entry1=Entry(screen2,textvariable=username_verify,width=20,font=("Arial",24))
    username_entry1.pack()
   # username_entry1.insert(0,"Login now")
    Label(screen2,text="").pack()

    Label(screen2,text="Password").pack()
    password_entry1=Entry(screen2,show="*",textvariable=password_verify,width=20,font=("Arial",24))
    password_entry1.pack()

    Label(screen2,text="").pack()
    Button(screen2,text="Login", width=12,height=1, command=login_verify).pack()








#The main Login/Register Screen  

def main_screen():
    global screen
    screen = Tk()
    screen.geometry("1080x1920")
    screen.title("3K04")
    Label(text="Welcome Back", fg="black",width="1920",height="4", font=("Calibri",50)).pack()
    Label(text="").pack()
    Button(text="Login",height="2",width="30",command=login).pack()
    Label(text="").pack()
    Button(text="Register",height="2",width="30",command=register).pack()
    screen.mainloop()

main_screen()
