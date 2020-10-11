#States
#1-TurnOn
#2-Connect
#3-Recording
#4-RecordedMotions
#5-ManualMotion
#6-Disconnect
#7-TurnOff

# import os
# import csv
# import pandas as pd
# from bluetooth import *
import time
# from dynamixel_sdk import *
# import dynamixel_functions as dynamixel
while True:

   
    def Connect():
        print("Speaker Project is Connected to the Phone via Bluetooth")
        state3 = input("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot:\n")
        if state3 == "R":
            Recording()
        elif state3 == "A":
            RecordedMotion()
        elif state3 == "M":
            ManualMode()
        elif state3 == "D":
            Disconnect()
        elif state4 == "F":
            TurnOff()

    def Recording():
        print("Motion is getting recorded")
        state4 = input("Please Complete Recording or Disconnect or Turn Off:\n")
        if state4 == "CR":
            RecordingComplete()
        elif state4 == "D":
            Disconnect()
        elif state4 == "F":
            TurnOff()
        
    def RecordingComplete():
        print("Motion Recording is complete and saved in the robot")
        state5 = input("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot:\n")
        if state5 == "R":
            Recording()
        elif state5 == "A":
            RecordedMotion()
        elif state5 == "M":
            ManualMode()
        elif state5 == "D":
            Disconnect()
        elif state5 == "F":
            TurnOff()
        
    def RecordedMotion():
        print("Recorded Motion is getting getting perfoAed")
        state6 = input("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot:\n")
        if state6 == "R":
            Recording()
        elif state6 == "A":
            RecordedMotion()
        elif state6 == "M":
            ManualMode()
        elif state6 == "D":
            Disconnect()
        elif state6 == "F":
            TurnOff()
            
    def ManualMode():
        print("Robot is in Manual Manipulation Mode")
        state7 = input("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot:\n")
        if state7 == "R":
            Recording()
        elif state7 == "A":
            RecordedMotion()
        elif state7 == "M":
            ManualMode()
        elif state7 == "D":
            Disconnect()
        elif state7 == "F":
            TurnOff()
        
    def Disconnect():
        print("Robot is disconnected from the phone")
        state8 = input("Please connect again or turn off:\n")
        if state8 == "C":
            Connect()
        elif state8 == "F":
            TurnOff()

    def TurnOff():
        print("Robot is turned off")
        state9 = input("Please Turn on:\n")
        if state9 == "O":
            TurnOn()
        else:
            print("Robot is still off")



    print("Speaker Project is Turned On")
    state2 = input("Please Connect your phone via BT:\n")
    if state2 == "C":
        Connect()
    else:
        print("the robot is not connected")
