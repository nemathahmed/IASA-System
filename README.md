# IASA-System
Immersive Acoustic Spatial Awareness System

## Requirements
*  python==3.7.4
*  pydub==0.23.1
*  darkflow==1.0.0
*  matplotlib==3.1.1                    
*  numpy==1.17.3                   
*  oauthlib==3.1.0                    
*  opencv-python==4.1.1.26
*  tensorflow==1.15.0
*  pygame==1.9.6
*  future==0.18.2
*  cython==0.29.14
*  cmake==3.15.3
*  pyserial==3.4


### Darflow Installation
* Translate darknet to tensorflow. Load trained weights, retrain/fine-tune using tensorflow, export constant graph def to mobile devices.
* Instruction to installation- https://github.com/thtrieu/darkflow
* YOLO weights from- https://drive.google.com/drive/folders/0B1tW_VtY7onidEwyQ2FtQVplWEU.

## Usage Guide
### Few important things:
* 1. A zone is the area in which the the obstacle might be located. Since we are using a 12 sensor array, we have divided the whole space into 12 zones spanning 10 degrees each.
* 2. Place the yolo model config file in darkflow/cfg as shown below
* 3. Input from the sensor is top-level i.e. even if YOLO Object detection misses on someitems detected by array, it is represented by a beep 
* The filed combine.py is a combination of files which include sound generation + obstacle detection + zonal sound generation and zonal obstacle detection.
* The function obstacledetection() hosts object detection multi layer Layer convnet which finally predicts the zonal possibile objects with 93.3% accuracy.
* The rest of the code is commented and is easy to follow
### Instructions
* Download the weights of YOLO and save it in the config and bin file of the darkflow folder. Absolute/relative location to the configuration files must be given accordingly.
* Individual beeps are placed in "..FINAL EDITS/" for 200Hz and "..FINAL EDITS 130HZ/" FOR 130 Hz.
* Individual file name follows "<number for degree> DEG.mp3" -- for example "FINAL EDITS/20 DEG.mp3" for a beep at 20 Deg with bass as 200Hz.
* Create an empty folder '/spec-sounds/' before you start anything.
  
  
  Made with :blue_heart: by Nocturnals
  
__author__ = "Team Nocturnals: Ahmed N., Polamaina S., Malick S."
__copyright__ = "Copyright (C) 2019 Nocturnals"
__version__ = "1.0"
