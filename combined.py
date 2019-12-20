# Copyright Info
__author__ = "Team Nocturnals: Ahmed N., Polamaina S., Malick S."
__copyright__ = "Copyright (C) 2019 Nocturnals"
__license__ = "Public Domain"
__version__ = "1.0"

#Library Requirements
from __future__ import print_function
import darkflow
from darkflow.net.build import TFNet
from gtts import gTTS 
import argparse, socket, sys,  binascii, struct, glob, collections
from collections import namedtuple
import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial
from serial import Serial
import time
from time import sleep
import sys
import pydub
pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
from pydub import AudioSegment
from pydub.playback import play
import os, winsound, subprocess,turtle
from threading import Thread                                                                  
from multiprocessing import Pool
processes = ('arc.py')

#Few important things:
#1. A zone is the area in which the the obstacle might be located. Since we are using a 12 sensor array, we have divided the whole space into 12 zones spanning 10 degrees each.
#2. Place the yolo model config file in darkflow/cfg as shown below
#3. Input from the sensor is top-level i.e. even if YOLO Object detection misses on someitems detected by array, it is represented by a beep 
options = {"model": "darkflow/cfg/yolo.cfg", 
           "load": "bin/yolo.weights", 
           "threshold": 0.1, 
           "gpu": 1.0}
tfnet = TFNet(options)
print('#########################################################################################################################')
# To create our zonal dictionary
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value        
def defaultdict():
    temp=my_dictionary()
    for i in range(12):
        temp.add(i,'None')
    return temp        
# Get angles from the sensor array
def getangles():
    print('Enter <Mode> <Angles>')
    arr=[str(x) for x in input().split()]
    return arr[0],arr[1:len(arr)]
#combine sounds to get a spatial map with base as 200Hz | mode-near
def combine(arr):
    print(arr,'yes')
    print("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+"BASE.mp3")
    soundbase=AudioSegment.from_mp3("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+str(arr[0])+" DEG.mp3")

    for i in range(0,len(arr)):
        print("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+str(arr[i])+" DEG.mp3")
        sound1 = AudioSegment.from_mp3("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+str(arr[i])+" DEG.mp3")
        soundbase = soundbase.overlay(sound1)
    return soundbase
#combine sounds to get a spatial map with base as 130Hz | mode-near
def combine_1(arr):
    print(arr,'yes')
    print("E:/Computer Vision/SoundLocalize/FINAL EDITS 130 HZ/BASE.mp3")
    soundbase=AudioSegment.from_mp3("E:/Computer Vision/SoundLocalize/FINAL EDITS 130 HZ/BASE.mp3")

    for i in range(0,len(arr)):
        print("E:/Computer Vision/SoundLocalize/FINAL EDITS 130 HZ/"+str(arr[i])+" DEG.mp3")
        sound1 = AudioSegment.from_mp3("E:/Computer Vision/SoundLocalize/FINAL EDITS 130 HZ/"+str(arr[i])+" DEG.mp3")
        soundbase = soundbase.overlay(sound1)
    return soundbase
#Export the final sound as finalmusic.wav
def export(soundfinal):
    soundfinal.export("finalmusic.wav", format='wav')
#Starughtforward playing of sound
def play_sound():
    winsound.PlaySound("finalmusic.wav", winsound.SND_ALIAS)
#YOLO for object detection multi layer Layer convnet
def obstacledetection():
    print('VP| Few moments..........')
    #cap = cv2.VideoCapture('rtsp://10.2.89.128:8080/h264_ulaw.sdp')
    #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
    #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 

    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter('./sample_video/output.avi',fourcc, 20.0, (int(width), int(height)))
    print('VP| Ready Now!')

    while(True):
        cap = cv2.VideoCapture('rtsp://10.2.89.128:8080/h264_ulaw.sdp')
        files = glob.glob('spec-sounds/*')
        for f in files:
           
            os.remove(f)
        
        print('Do you have the zonal array 1-Yes/0-no')
        doihavezonearray=int(input())
        if(doihavezonearray==0):
            print('Input any number to start an iteration')
            p=int(input())
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret == True:
                
                frame = np.asarray(frame)
                results = tfnet.return_predict(frame)

                arr=[]
                points=[]
                print('VP| Analyzing')
                
                # Display the resulting frame
                total_object=len(results)
                ilen=1
                final=defaultdict()
                for result in results:
                    print('Processed ',(ilen/total_object)*100,'%', end="\r")
                    ilen=ilen+1
                
                    arr.append(result['label'])
                    tl,br = (result['topleft']['x'],result['bottomright']['x'])
                    points.append((tl+br)/2)
                    zone=int(((tl+br)/2)/160)
                    final[zone]= result['label']
                    #print(result['label'],zone)
                    
                od = collections.OrderedDict(sorted(final.items()))
                print('VP| ',od)
                #print(arr)
                print('VP| Analyzed!!')

                for key in od:
                    areaindeg=key*10-60
                    if(areaindeg<0):
                        Name=str(od[key]) #+'at negative'+ str(areaindeg)
                    else:
                        Name=str(od[key]) #+'at positive'+ str(areaindeg)

                    myobj = gTTS(text=Name, lang='en', slow=False)
                    if od[key]=='None':
                        #Name1='No object' 
                        #sil = gTTS(text=Name1, lang='en', slow=False)
                        #sil.save('spec-sounds/'+str(key)+'.mp3')
                        continue
                    else:
                        myobj.save('spec-sounds/'+str(key)+'.mp3')
                    #song = AudioSegment.from_mp3("myjarvissound.mp3")
                    #play(song)
                noarrayobstacledetector()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        else:
            print('enter the array')
            zonalarray=[int(x) for x in input().split()]
            print('Input any number 1-9 to start an iteration and 0 to end')
            p=int(input())
            if p==0:
                break
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret == True:
                
                frame = np.asarray(frame)
                results = tfnet.return_predict(frame)

                arr=[]
                points=[]
                print('VP| Analyzing')
                
                # Display the resulting frame
                total_object=len(results)
                ilen=1
                final=defaultdict()
                for result in results:
                    print('Processed ',(ilen/total_object)*100,'%', end="\r")
                    ilen=ilen+1
                
                    arr.append(result['label'])
                    tl,br = (result['topleft']['x'],result['bottomright']['x'])
                    points.append((tl+br)/2)
                    zone=int(((tl+br)/2)/160)
                    final[zone]= result['label']
                    #print(result['label'],zone)
                    
                od = collections.OrderedDict(sorted(final.items()))
                print('VP| ',od)
                #print(arr)
                print('VP| Analyzed!!')

                for key in od:
                    areaindeg=key*10-60
                    if(areaindeg<0):
                        Name=str(od[key]) #+'at negative'+ str(areaindeg)
                    else:
                        Name=str(od[key]) #+'at positive'+ str(areaindeg)

                    myobj = gTTS(text=Name, lang='en', slow=False)
                    if od[key]=='None':
                        #Name1='No object' 
                        #sil = gTTS(text=Name1, lang='en', slow=False)
                        #sil.save('spec-sounds/'+str(key)+'.mp3')
                        continue
                    else:
                        myobj.save('spec-sounds/'+str(key)+'.mp3')
                    #song = AudioSegment.from_mp3("myjarvissound.mp3")
                    #play(song)
                noarrayobstacledetector(zonalarray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break


    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()     
#Generating a complete 3D map without any relation to zonal array 
def noarrayobstacledetector():
    base=AudioSegment.from_mp3("BASE.mp3")
    base.export('mode2-3dvision.mp3',format='mp3')
    #time=2495
    time=0
    #sound=AudioSegment.from_mp3('spec-sounds/' +str(0)+'.mp3')
    #base=base.overlay(sound,position=time)

    for i in range(0,12):
        try:
            sound=AudioSegment.from_mp3('spec-sounds/' + str(i)+ '.mp3')
            base=base.overlay(sound,position=time)
            base.export('mode2-3dvision.mp3',format='mp3')
            base=AudioSegment.from_mp3('mode2-3dvision.mp3')
            time=time+1000

        except FileNotFoundError:
            time=time+1000
            continue

    #base.export('mode2-3dvision.mp3',format='mp3')
    song = AudioSegment.from_mp3("mode2-3dvision.mp3")
    play(song)
#Generating 3D map when manually fed with zonal array data
def noarrayobstacledetector(zonalarray):
    base=AudioSegment.from_mp3("BASE.mp3")
    base.export('mode2-3dvision.mp3',format='mp3')
    #time=2495
    time=0
    #sound=AudioSegment.from_mp3('spec-sounds/' +str(0)+'.mp3')
    #base=base.overlay(sound,position=time)

    for i in range(0,12):
        try:
            if (i in zonalarray):
                sound=AudioSegment.from_mp3('spec-sounds/' + str(i)+ '.mp3')
                base=base.overlay(sound,position=time)
                base.export('mode2-3dvision.mp3',format='mp3')
                base=AudioSegment.from_mp3('mode2-3dvision.mp3')
                time=time+1000
            else:
                
                    
                time=time+1000
                continue
        
        except FileNotFoundError:
            if(i in zonalarray):
                    sound1=AudioSegment.from_wav('beep.wav')
                    base=base.overlay(sound1,position=i*1000)
                    base.export('mode2-3dvision.mp3',format='mp3')
                    base=AudioSegment.from_mp3('mode2-3dvision.mp3')
            time=time+1000
            continue
    
    #base.export('mode2-3dvision.mp3',format='mp3')
    song = AudioSegment.from_mp3("mode2-3dvision.mp3")
    play(song)
#Generating 3D map taking direct zonal information from sensorarray
def withobstaclearraydetector(marr):
    base=AudioSegment.from_mp3("BASE.mp3")
    time=2495
    sound=AudioSegment.from_mp3('spec-sounds/' +str(marr[0])+ '.mp3')
    base=base.overlay(sound,time)

    for i in marr[1:]:
        time=time+208
        sound=AudioSegment.from_mp3('spec-sounds/' +str(i)+ '.mp3')
        base=base.overlay(sound,position=time)
    base.export('mode2-3dvision.mp3',format='mp3')
    song = AudioSegment.from_mp3("mode2-3dvision.mp3")
    play(song)

#Main Program
print('Ready Now!')
while True:
    print('Input 0 for obstacle-detection info and 1 for obstacle-identification(detailed) info')
    turtle.bye()
    detection_or_identification=int(input())
    if(detection_or_identification==0):
        print('Input 1 if connected with the sensor array')
        doihavearray=int(input())
        if(doihavearray==1):
            #COM is the COM port being used with Arduino Mega
            COM = 'COM3'
            BAUD = 9600 #Baud rate!

            ser = serial.Serial(COM, BAUD, timeout = 0.1)

            print("Waiting for device")
            sleep(12)
            print(ser.name)
            try:
                val = str(ser.readline().decode().strip("\r\n"))
               
            except UnicodeDecodeError:
                print("uh oh")
            
            try:
                arr=[]
                print(val)
                val=list(val)
                for i in range(len(val)):
                    if val[i]==':':
                        arr.append(val[i+1])

                print('arr ',arr)

                finalarr=[]
                finalarr.append(0)
                for j in range(len(arr)):
                    if int(arr[j])==0:
                        finalarr.append(-60+10*(j+1))
                print(finalarr, end = "\n", flush = True)
                mode,angle_arr=0,finalarr[1:len(finalarr)]
                print(mode,angle_arr)
                if int(mode)==0:
                    final=combine(angle_arr)
                    export(final)
                elif int(mode)==1:
                    final=combine_1(angle_arr)
                    export(final)
                arr_int=[]
                for i in range(len(angle_arr)):
                    arr_int.append(int(angle_arr[i]))
                #multithreading to play and view the map
                for i in range(1):
                    thread = Thread(target=play_sound)
                    thread.start()
                # uncomment below lines to view map using turtle
                '''
                radius=300
                angle=-70
                turtle.speed('fastest')
                turtle.setpos(-285,93)
                for i in range(140):
                #print(int(angle))
                    theta=(angle*np.pi)/180
                    #print('imhere',theta)
                    if int(angle) in finalarr:
                        print('Angle ',angle,'Processed')
                        turtle.write(int(angle))
                    turtle.setpos(300*np.sin(theta),300*np.cos(theta))
                    time.sleep(0.06550)
            
                    angle=angle+1


            
            '''
            except NameError:
                print("not again")
            sleep(5)
            #turtle.bye()
            ser.close()
        else:
            # Manual zonal entry
            print('enter the [mode,angle1,angle2,angle3...]')
            modeanglearray=[int(x) for x in input().split()]
            mode,angle_arr=modeanglearray[0],modeanglearray[1:]
            print(mode,angle_arr)
            if int(mode)==0:
                final=combine(angle_arr)
                export(final)
            elif int(mode)==1:
                final=combine_1(angle_arr)
                export(final)
            arr_int=[]
            for i in range(len(angle_arr)):
                arr_int.append(int(angle_arr[i]))
            
            for i in range(1):
                thread = Thread(target=play_sound)
                thread.start()
            
            # uncomment below lines to view map using turtle
            '''
            radius=300
            angle=-70
            
            turtle.speed('fastest')
            turtle.setpos(-285,93)
            
            for i in range(140):
                #print(int(angle))
                theta=(angle*np.pi)/180
                   #print('imhere',theta)
                if int(angle) in arr_int:
                    print('Angle ',angle,'Processed')
                    turtle.write(int(angle))
                turtle.setpos(300*np.sin(theta),300*np.cos(theta))
                time.sleep(0.06550)
            
                angle=angle+1
            turtle.bye()
            ''''
    if(detection_or_identification==1):
        print('Do you have sensor array| 1 for yes 0 for no')
        doihavearray=int(input())
        if(doihavearray==1):
            obstacledetection()
            COM = 'COM3'
            BAUD = 9600

            ser = serial.Serial(COM, BAUD, timeout = 0.1)

            print("Waiting for device")
            sleep(3)
            print(ser.name)
            try:
                val = str(ser.readline().decode().strip("\r\n"))
                #val = str(ser.readline())
            except UnicodeDecodeError:
                print("uh oh")
            #valA = val.split("/")
            try:
                arr=[]
                val=list(val)
                for i in range(len(val)):
                    if val[i]==':':
                        arr.append(val[i+1])

                finalarr=[]
                finalarr.append(0)
                for j in range(len(arr)):
                    if int(arr[j])==0:
                        
                        finalarr.append(-60+10*(j+1))
                print(finalarr, end = "\n", flush = True)
                mode,angle_arr=0,finalarr[1:len(arr)]
                print(mode,angle_arr)
                if int(mode)==0:
                    final=combine(angle_arr)
                    export(final)
                elif int(mode)==1:
                    final=combine_1(angle_arr)
                    export(final)
                arr_int=[]
                for i in range(len(angle_arr)):
                    arr_int.append(int(angle_arr[i]))
            
                for i in range(1):
                    thread = Thread(target=obstacledetection)
                    thread.start()


                withobstaclearraydetector(arr_int)
            
                '''
                radius=300
                angle=-70
                turtle.speed('fastest')
                turtle.setpos(-285,93)
                for i in range(140):
                #print(int(angle))
                    theta=(angle*np.pi)/180
                    #print('imhere',theta)
                    if int(angle) in finalarr:
                        print('Angle ',angle,'Processed')
                        turtle.write(int(angle))
                    turtle.setpos(300*np.sin(theta),300*np.cos(theta))
                    time.sleep(0.06550)
            
                    angle=angle+1
                '''

            except NameError:
                print("not again")
            sleep(5)
        else:
            obstacledetection()
            print('finished')
    else:
        print('Try Again')
        continue