#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from Tkinter import Tk, W, E, S, N
from ttk import Frame, Button, Label, Style
from ttk import Entry
 
import serial
import time
import os
from random import randint
 
from Tkinter import *
 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
 
import time
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
 
# serial.Serial(port, bps, bytesize, parity bit, stopp bit, timeout)
ser = serial.Serial('COM39',115200, 8, serial.PARITY_NONE, 1,0) # ser is the variable for the serial port, i.e. bluetooth
ser.flushInput()
 
irsens = [0, 0, 0, 0, 0]
rsens = [0, 0]
alpha = [0, 0]
omega2 = 0
counter = 0
test_counter = 0
hjul = 0
directions = 0
u = 0
e_styr = 0
alpha_styr = 0
driven_distance= 0
ddcorner = 0
command = ''
xdir = 0
ydir = 0
robo_pos_x = 0
robo_pos_y = 0
goal_coord_x=0
goal_coord_y=0
 
driveable = [[0 for x in range(15)] for x in range(15)]
explored = [[0 for i in range(15)] for i in range(15)]
 
def quit(ser):
    ser.close()
 
def get_bit(x,n):
    if (x & 2**n != 0):
        return 1
    else:
        return 0
 
def get_byte(driveable, val, row, column):
        driveable[row][column] = get_bit(val,0)
        driveable[row][column+1] = get_bit(val,1)
        driveable[row][column+2] = get_bit(val,2)
        driveable[row][column+3] = get_bit(val,3)
        driveable[row][column+4] = get_bit(val,4)
        return driveable
 
def updateValues(sens, val):
    global u
    global omega1
    global hjul
    global rsens
    global omega2
    global directions
    global e_styr
    global alpha_styr
    global test_counter
    global driven_distance
    global command
    global robo_pos_x
    global robo_pos_y
    global goal_coord_x
    global goal_coord_y
    global xdir
    global ydir
    global driveable
    global explored
    global ddcorner
     
    if (sens == 255):
        irsens[0] = val/5.0
    elif (sens == 254):
        irsens[1] = val/5.0
    elif (sens == 253):
        irsens[2] = val/5.0
    elif (sens == 252):
        irsens[3] = val/5.0
    elif (sens == 251):
        irsens[4] = val/5.0
    elif (sens == 250):
        hjul = hjul
    elif (sens == 249):
        rsens[1] = val
    elif (sens == 246):
        #printSens() 
        test_counter = val
    #elif (sens == 246):
        #alpha[0] = val/5.0
    elif (sens == 245):
        alpha[1] = val/5.0
    #elif(sens==248):
        #omega1 = val/5.0
    elif (sens == 248):
        directions = val
        ddcorner = driven_distance
        printSens()
    elif(sens== 247):
        omega2 = val/5.0
    elif(sens == 239):
        driven_distance = val
    elif(sens == 238):
        driveable = get_byte(driveable, val, 0, 0)
    elif(sens == 237):
        driveable = get_byte(driveable, val, 0, 5)
    elif(sens == 236):
        driveable = get_byte(driveable, val, 0, 10)
    elif(sens == 235):
        driveable = get_byte(driveable, val, 1, 0)
    elif(sens == 234):
        driveable = get_byte(driveable, val, 1, 5)
    elif(sens == 233):
        driveable = get_byte(driveable, val, 1, 10)
    elif(sens == 232):
        driveable = get_byte(driveable, val, 2, 0)
    elif(sens == 231):
        driveable = get_byte(driveable, val, 2, 5)
    elif(sens == 230):
        driveable = get_byte(driveable, val, 2, 10)
    elif(sens == 229):
        driveable = get_byte(driveable, val, 3, 0)
    elif(sens == 228):
        driveable = get_byte(driveable, val, 3, 5)
    elif(sens == 227):
        driveable = get_byte(driveable, val, 3, 10)
    elif(sens == 226):
        driveable = get_byte(driveable, val, 4, 0)
    elif(sens == 225):
        driveable = get_byte(driveable, val, 4, 5)
    elif(sens == 224):
        driveable = get_byte(driveable, val, 4, 10)
    elif(sens == 223):
        driveable = get_byte(driveable, val, 5, 0)
    elif(sens == 222):
        driveable = get_byte(driveable, val, 5, 5)
    elif(sens == 221):
        driveable = get_byte(driveable, val, 5, 10)
    elif(sens == 220):
        driveable = get_byte(driveable, val, 6, 0)
    elif(sens == 219):
        driveable = get_byte(driveable, val, 6, 5)
    elif(sens == 218):
        driveable = get_byte(driveable, val, 6, 10)
    elif(sens == 217):
        driveable = get_byte(driveable, val, 7, 0)
    elif(sens == 216):
        driveable = get_byte(driveable, val, 7, 5)
    elif(sens == 215):
        driveable = get_byte(driveable, val, 7, 10)
    elif(sens == 214):
        driveable = get_byte(driveable, val, 8, 0)
    elif(sens == 213):
        driveable = get_byte(driveable, val, 8, 5)
    elif(sens == 212):
        driveable = get_byte(driveable, val, 8, 10)
    elif(sens == 211):
        driveable = get_byte(driveable, val, 9, 0)
    elif(sens == 210):
        driveable = get_byte(driveable, val, 9, 5)
    elif(sens == 209):
        driveable = get_byte(driveable, val, 9, 10)
    elif(sens == 208):
        driveable = get_byte(driveable, val, 10, 0)
    elif(sens == 207):
        driveable = get_byte(driveable, val, 10, 5)
    elif(sens == 206):
        driveable = get_byte(driveable, val, 10, 10)
    elif(sens == 205):
        driveable = get_byte(driveable, val, 11, 0)
    elif(sens == 204):
        driveable = get_byte(driveable, val, 11, 5)
    elif(sens == 203):
        driveable = get_byte(driveable, val, 11, 10)
    elif(sens == 202):
        driveable = get_byte(driveable, val, 12, 0)
    elif(sens == 201):
        driveable = get_byte(driveable, val, 12, 5)
    elif(sens == 200):
        driveable = get_byte(driveable, val, 12, 10)
    elif(sens == 199):
        driveable = get_byte(driveable, val, 13, 0)
    elif(sens == 198):
        driveable = get_byte(driveable, val, 13, 5)
    elif(sens == 197):
        driveable = get_byte(driveable, val, 13, 10)
    elif(sens == 196):
        driveable = get_byte(driveable, val, 14, 0)
    elif(sens == 195):
        driveable = get_byte(driveable, val, 14, 5)
    elif(sens == 194):
        driveable = get_byte(driveable, val, 14, 10)
    elif(sens == 176):
        command = val
    elif(sens == 177):
        robo_pos_x = val
    elif(sens == 178):
        robo_pos_y = val
        #printSens()
    elif(sens == 179):
        xdir = val-5
    elif(sens == 180):
        ydir = val-5
    elif (sens == 242):
        goal_coord_y = val
    elif (sens == 241):
        goal_coord_x = val
    elif(sens == 174):
        explored = get_byte(explored, val, 0, 0)
    elif(sens == 173):
        explored = get_byte(explored, val, 0, 5)
    elif(sens == 172):
        explored = get_byte(explored, val, 0, 10)
    elif(sens == 171):
        explored = get_byte(explored, val, 1, 0)
    elif(sens == 170):
        explored = get_byte(explored, val, 1, 5)
    elif(sens == 169):
        explored = get_byte(explored, val, 1, 10)
    elif(sens == 168):
        explored = get_byte(explored, val, 2, 0)
    elif(sens == 167):
        explored = get_byte(explored, val, 2, 5)
    elif(sens == 166):
        explored = get_byte(explored, val, 2, 10)
    elif(sens == 165):
        explored = get_byte(explored, val, 3, 0)
    elif(sens == 164):
        explored = get_byte(explored, val, 3, 5)
    elif(sens == 163):
        explored = get_byte(explored, val, 3, 10)
    elif(sens == 162):
        explored = get_byte(explored, val, 4, 0)
    elif(sens == 161):
        explored = get_byte(explored, val, 4, 5)
    elif(sens == 160):
        explored = get_byte(explored, val, 4, 10)
    elif(sens == 159):
        explored = get_byte(explored, val, 5, 0)
    elif(sens == 158):
        explored = get_byte(explored, val, 5, 5)
    elif(sens == 157):
        explored = get_byte(explored, val, 5, 10)
    elif(sens == 156):
        explored = get_byte(explored, val, 6, 0)
    elif(sens == 154):
        explored = get_byte(explored, val, 6, 5)
    elif(sens == 153):
        explored = get_byte(explored, val, 6, 10)
    elif(sens == 152):
        explored = get_byte(explored, val, 7, 0)
    elif(sens == 151):
        explored = get_byte(explored, val, 7, 5)
    elif(sens == 150):
        explored = get_byte(explored, val, 7, 10)
    elif(sens == 149):
        explored = get_byte(explored, val, 8, 0)
    elif(sens == 148):
        explored = get_byte(explored, val, 8, 5)
    elif(sens == 147):
        explored = get_byte(explored, val, 8, 10)
    elif(sens == 146):
        explored = get_byte(explored, val, 9, 0)
    elif(sens == 145):
        explored = get_byte(explored, val, 9, 5)
    elif(sens == 143):
        explored = get_byte(explored, val, 9, 10)
    elif(sens == 142):
        explored = get_byte(explored, val, 10, 0)
    elif(sens == 141):
        explored = get_byte(explored, val, 10, 5)
    elif(sens == 140):
        explored = get_byte(explored, val, 10, 10)
    elif(sens == 139):
        explored = get_byte(explored, val, 11, 0)
    elif(sens == 138):
        explored = get_byte(explored, val, 11, 5)
    elif(sens == 137):
        explored = get_byte(explored, val, 11, 10)
    elif(sens == 136):
        explored = get_byte(explored, val, 12, 0)
    elif(sens == 135):
        explored = get_byte(explored, val, 12, 5)
    elif(sens == 134):
        explored = get_byte(explored, val, 12, 10)
    elif(sens == 133):
        explored = get_byte(explored, val, 13, 0)
    elif(sens == 132):
        explored = get_byte(explored, val, 13, 5)
    elif(sens == 131):
        explored = get_byte(explored, val, 13, 10)
    elif(sens == 130):
        explored = get_byte(explored, val, 14, 0)
    elif(sens == 129):
        explored = get_byte(explored, val, 14, 5)
    elif(sens == 128):
        explored = get_byte(explored, val, 14, 10)
         
 
 
 
         
    else:
        pass
        #print "Not ir- or r-sensor."
 
'''def printSens():
    print "right back: ", irsens[0], "right front: ", irsens[1], "nfront: ", irsens[2], "nleft back: ", irsens[4], "left front: ", irsens[3], 
    print "Bak = ", omega2
    print "Hjul: ", hjul, "M�l: ", rsens[1]
    print "u =", u
    print "inWaiting: ", ser.inWaiting()
    print "Sp�nning h�ger bak: ", test_counter
    print "Possible directions :", directions
    print "K�rd str�cka: ", driven_distance
    for x in range(0,15):
        print driveable[x]
    print "-----------------------"
    '''
 
def printSens():
    print "nnnn"
          "-----------------------------------------------------------------------------------------", "n", 
          driveable[:][14], " " , explored[:][14],  "            Front: ", irsens[2], "n", 
          driveable[:][13], " " , explored[:][13],  "    Left front:  ", irsens[3], " | Right front: ", irsens[1], "n",  
          driveable[:][12], " " , explored[:][12],  "    Left back:  ",  irsens[4], " | Right back: ", irsens[0], "n", 
          driveable[:][11], " " , explored[:][11],  "            Back: ", omega2,  "n", 
          driveable[:][10], " " , explored[:][10],  "n", 
          driveable[:][9], " " , explored[:][9],  "    Hjul:       ", hjul,            " | Mal:         ", rsens[1],  "n",  
          driveable[:][8], " " , explored[:][8],  "    inWaiting   ", ser.inWaiting(), " | u:           ", u, "n", 
          driveable[:][7], " " , explored[:][7],  "", "n", 
          driveable[:][6], " " , explored[:][6],  "    Possible directions: ", directions, "n", 
          driveable[:][5], " " , explored[:][5],  "    Driven_distance: ", driven_distance, "|    ddc: ", ddcorner, "n", 
          driveable[:][4], " ", explored[:][4], "    Command: ", command, "n", 
          driveable[:][3], " ", explored[:][3], "", "n", 
          driveable[:][2], " ", explored[:][2], "        FWALL:             pos: (", robo_pos_x, ", ", robo_pos_y, ")", "n", 
          driveable[:][1], " ", explored[:][1], "    LWALL: ", "  RWALL:     x,y-dir: (", xdir, ", ", ydir, ")", "n", 
          driveable[:][0], " ", explored[:][0], "        BWALL: ",  "Goal position: (", goal_coord_x,",", goal_coord_y, ")", "n", 
          "----------------------------------------------------------------------------------------"
 
     
'''
def BluetoothUpdate(counter):
    time.sleep(0.0001)
    #print ser.inWaiting()
    temp = ser.read(1)
    #print "!"
    data = []
 
    if (ser.inWaiting() > 400):
        ser.flushInput()                                     
    for i in range(0, len(temp)):
        data.append(ord(temp[i]))
     
    if (len(data) == 1):
        #print "Hej"
        time.sleep(0.0000001)
        if (data[0] >= 220): #& (data[1]<242)
            #print data
            sens = data[0]
            val = ser.read(1)
            while len(val) == 0:
                val = ser.read(1)
                time.sleep(0.0000001)
            if ord(val) < 220:
                updateSens(sens, ord(val))
    if (counter == 49999):
        printSens()
'''
 
'''
def BluetoothUpdate(counter):
    time.sleep(0.0001)
    #print ser.inWaiting()
    temp = ser.read(3)
    data = []
    for i in range(0, len(temp)):
        data.append(ord(temp[i]))
     
    if (ser.inWaiting() > 400):
        ser.flushInput()                                     
   
    if (len(data) == ):
        time.sleep(0.0000001)
        if (data[0] >= 220):
            sens = data[0]
            if data[1] < 220:
                updateSens(sens, data[1])
    if (counter == 49999):
        pass
        printSens()
'''
 
def BluetoothUpdate(counter):
    time.sleep(0.0001)
    #print ser.inWaiting()
    temp = ser.read(1)
    if (len(temp) == 1):
        if (ord(temp) == 0):
            temp = ser.read(2)
            data = []
            for i in range(0, len(temp)):
                data.append(ord(temp[i]))
           
            if (len(data) == 2 ):
                time.sleep(0.0000001)
                updateValues(data[0], data[1])
                 
    if (counter == 19999):
        printSens()
       
    if (ser.inWaiting() > 1000):
        ser.flushInput()
         
while(1):
    BluetoothUpdate(counter)
    counter+=1
    if counter == 20000:
        counter = 0
     