import pydub
pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
from pydub import AudioSegment
from pydub.playback import play
import turtle
from threading import Thread
import numpy as np
import time
import winsound    
def play_sound():
    winsound.PlaySound("finalmusic.wav", winsound.SND_ALIAS)   
def export(soundfinal):
    soundfinal.export("finalmusic.wav", format='wav')
def combine(arr):
    print(arr,'yes')
    print("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+"BASE.mp3")
    soundbase=AudioSegment.from_mp3("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+str(arr[0])+" DEG.mp3")

    for i in range(0,len(arr)):
        print("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+str(arr[i])+" DEG.mp3")
        sound1 = AudioSegment.from_mp3("E:/Computer Vision/SoundLocalize/FINAL EDITS/"+str(arr[i])+" DEG.mp3")
        soundbase = soundbase.overlay(sound1)
    return soundbase



print('enter the [mode,angle1,angle2,angle3...]')
modeanglearray=[int(x) for x in input().split()]
mode,angle_arr=modeanglearray[0],modeanglearray[1:]
print(mode,angle_arr)
if int(mode)==0:
    final=combine(angle_arr)
    export(final)

arr_int=[]
for i in range(len(angle_arr)):
    arr_int.append(int(angle_arr[i]))

for i in range(1):
    thread = Thread(target=play_sound)
    thread.start()

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