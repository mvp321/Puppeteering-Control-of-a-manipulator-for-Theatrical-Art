#States
#1-TurnOn
#2-Connect
#3-Recording
#4-RecordedMotions
#5-ManualMotion
#6-Disconnect
#7-TurnOff

#All functions:
#ChangeSpeed_AX(DXL_ID,speed)
#ChangeSpeed_MX(DXL_ID,speed)
#move_motor(goal_Pos, speed=20)
#read_ax(ID,ID1,ID2)
#readspeed(ID,ID1, ID2)
#writefile(ID,dxl_present_position,ID1,dxl_present_position1,ID2,dxl_present_position2)
#readfile()
#calculating_speed(new_pos,old_pos)
#home_config(goal_Pos1,goal_Pos2,goal_Pos3)
#read(DXL1_ID,DXL2_ID)
#check_position_reached(goal_Pos ,goal_Pos1 ,goal_Pos2)
#check_threshold(goal_Pos, dxl_present_position,ID)

#main While loop
import time
import os
import csv
#import pandas as pd
from bluetooth import *
import time
from dynamixel_sdk import *
from datetime import datetime
#import dynamixel_functions as dynamixel

#================================================
# VARIABLES and CONSTANTS

#DEFINE 

#1) TurnOn state:
#def TurnOn():
ADDR_MX_TORQUE_ENABLE = 24  # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36
LEN_MX_PRESENT_POSITION     = 2
count = 0
tic = time.perf_counter()
dt = datetime.now()
minimum_value_mx64 = 400    #this is 35.2 degrees
maximum_value_mx64 = 2350   #this is 211.2 degrees
minimum_value_ax12 = 200    #this is 90 degrees
maximum_value_ax12 = 500   #this is 180 degrees
#minimum_value_ax12 =
#maximum_value_ax12 = 
# Protocol version
PROTOCOL_VERSION = 1.0  # See which protocol version is used in the Dynamixel
# Default setting
# Dynamixel ID : 1
BAUDRATE = 1000000  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'  # Check which port is being used on your controller                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque

DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold
port_num = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
COM_SUCCESS = 0
COM_TX_FAIL = -1001
filename = "routines.csv"

sampling_rate = 0.22 #seconds

state = "D"     # Turn on State
# =============================================================

# RUN ONCE
Setup()

data = ''
# ==================================================


while True:  

    command = CheckCommand()    # check the command from the app

    #press connect to connect after this point
    if state == "D":
        Connect()
    elif state == "C":
        if command == "M":
            ManualMode()
        elif command == "A":    # check info[1] for fileName
            MotionPlayback()
        elif command == "R":
            MotionRecord()      # check info[1] for fileName
        elif command == "F":    # run the "Shutdown sequence". Home position, then  turn off Rpi. 
            TurnOff()
        elif command == "S":    # Stop the recording of motion and close the file. State goes to C
            StopRecord()

def Setup():
      "Opening the port and setting the baudrate"
    if port_num.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to teAinate...")
        quit()
    # Set port baudrate
    if port_num.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to teAinate...")
        quit()
    "just to check the connection"
    DXL_ID = [1,2,3]

    "enabling the torque and checking if dynamixel is connected"
    dxl_coM_result, dxl_error = packetHandler.write1ByteTxRx(port_num, DXL_ID[1], ADDR_MX_TORQUE_ENABLE, 0)  # TORQUE_DISABLE
    if dxl_coM_result != COM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_coM_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

def CheckCommand():
    state = info[0]

def DataRead():
    data += client_socket.recv(1024).decode("utf-8")
    if data[-1] == '\n':
        print(data)
        info = data.split(',')
        data = ''

def Disconnect():
    print("Robot is disconnected from the phone")
    if state == "C":
        Connect()
    else:
        print("the robot is still connected")

#2) Connect State:            
def Connect():
    print("Speaker Project is Connected to the Phone via Bluetooth")
    print("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot")

    # Add  bluetooth connection code
    isconnected = BtConnect()
    
    if isconnected == True:
        state = "C"
    else:
        state = "D"

def BtConnect():
    data = '' 
    server_socket = BluetoothSocket(RFCOM)
    port = 1
    server_socket.bind(("",port))
    server_socket.listen(1)
    print("Please Connect your phone via BT")

    try:

        client_socket,address = server_socket.accept()
        print ("Accepted connection from ",address)
        return True

    except:
        print("Doesn't connect")
        return False
        
#3) Recording Motion Mode:
def Recording():
    #read_ax(1,2,3)
    print("Motion is getting recorded")
    print("Please Complete Recording or Disconnect or Turn Off")
    state = info[0]
    if state == "S":
        RecordingComplete()
    elif state == "D":
        Disconnect()
    elif state == "F":
        TurnOff()
    
def MotionRecord():
    csvfile.close()
    print("Motion Recording is complete and saved in the robot")
    print("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot")
    state = info[0]
    if state == "R":
        Recording()
    elif state == "A":
        RecordedMotion()
    elif state == "M":
        ManualMode()
    elif state == "D":
        Disconnect()
    elif state == "F":
        TurnOff()

def StopRecord():
    print("Stop the recording")
    #close the file
    state = "C"
    
def MotionPlayback():
    #readfile()
    print("Recorded Motion is getting performed")
    print("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot")
    state = info[0]
    if state == "R":
        Recording()
    elif state == "A":
        RecordedMotion()
    elif state == "M":
        ManualMode()
    elif state == "D":
        Disconnect()
    elif state == "F":
        TurnOff()
        
def ManualMode():
    #move_motor(512)
    print("Robot is in Manual Manipulation Mode")
    
    if info[0] == "1":
        angle1 = int((2047*int(info[1]))/180)
        move_motor(angle1)

    if info[0] == "2":
        if info[1]=="0":
            angle2 = 400
        elif info[1] =="180":
            angle2 = 2350
        else:
            angle2 = int(minimum_value_mx64 + ((maximum_value_mx64 - minimum_value_mx64)/180)*int(info[1]))
        move_motor(angle2)

    if info[0] == "3":
        if info[1]=="90" or int(info[1]) < 90:
            angle3 = 200
        elif info[1] =="180" or int(info[1]) > 180:
            angle3 = 500
        else:
            angle3 = int(((maximum_value_ax12 - minimum_value_ax12)/90)*int(info[1])-100)
        move_motor(angle3)
            
    print("Please Choose between Record, Recorded Motion and Manual Mode or Disconnect the robot")
    
    if info[0] == "R":
        Recording()
    elif info[0] == "A":
        RecordedMotion()
    elif info[0] == "M":
        ManualMode()
    elif info[0] == "D":
        Disconnect()
    elif info[0] == "F":
        TurnOff()
    


def TurnOff():
    groupBulkRead.clearParam()
    port_num.closePort()
    client_socket.close()
    server_socket.close()
    print("Robot is turned off")


def move_motor(goal_Pos, speed=20):
    DXL_ID = int(info[0])
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, DXL_ID, ADDR_MX_GOAL_POSITION, goal_Pos)
    if dxl_comm_result != COMM_SUCCESS:
        print("THIS IS THE PROBLEM 1")
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("THIS IS THE PROBLEM 2")
    else:
        print("THIS IS OK!")
    time.sleep(0.2)
    
    "reading the present position and stopping if threshold is lower than 20"
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, DXL_ID, ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, goal_Pos, dxl_present_position))

        if not abs(goal_Pos - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            return
    else:
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, goal_Pos, dxl_present_position))
    
    global dxl_load
    dxl_load, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, DXL_ID, 40)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("[ID:%03d] GoalPos:%03d  Load:%03d" % (DXL_ID, goal_Pos, dxl_load))
        return dxl_load
        

def read_ax(ID,ID1,ID2):
    count = 0
    open(filename, 'w').close()
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, ID, ADDR_MX_TORQUE_ENABLE, 0)
    dxl_comm_result1, dxl_error1 = packetHandler.write1ByteTxRx(port_num, ID1, ADDR_MX_TORQUE_ENABLE, 0)
    dxl_comm_result2, dxl_error2 = packetHandler.write1ByteTxRx(port_num, ID2, ADDR_MX_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % ID)

    while 1:
        time1 = time.time()
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, ID, ADDR_MX_PRESENT_POSITION)
        dxl_present_position1, dxl_comm_result1, dxl_error1 = packetHandler.read2ByteTxRx(port_num, ID1, ADDR_MX_PRESENT_POSITION)
        dxl_present_position2, dxl_comm_result2, dxl_error2 = packetHandler.read2ByteTxRx(port_num, ID2, ADDR_MX_PRESENT_POSITION)
        
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            #print("[ID:%03d] PresPos:%03d" % (ID, dxl_present_position))
            #return dxl_present_position 
            #print("[ID:%03d] PresPos:%03d" % (ID1, dxl_present_position1))
            if writefile(ID,dxl_present_position,ID1,dxl_present_position1,ID2,dxl_present_position2) == 1:
                #print("this has been broken")
                break
            delaytime = time.time() - time1            
            time.sleep(sampling_rate - delaytime)
            print("time delay while storing",delaytime)
            #print("time is",time.time()-time1)


def readspeed(ID,ID1, ID2):
    dxl_speed, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, ID, 38)
    dxl_speed1, dxl_comm_result1, dxl_error1 = packetHandler.read2ByteTxRx(port_num, ID1, 38)
    dxl_speed2, dxl_comm_result2, dxl_error2 = packetHandler.read2ByteTxRx(port_num, ID2, 38)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        return 6000,6000, 6000
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        return 6000,6000, 6000
    else:
        #print("[ID:%03d] Speed:%03d" % (ID, dxl_speed))
        #print("[ID:%03d] Speed:%03d" % (ID1, dxl_speed1))
        return dxl_speed,dxl_speed1, dxl_speed2


def writefile(ID,dxl_present_position,ID1,dxl_present_position1,ID2,dxl_present_position2):
    fields = ['ID','motor_pos','speed','ID1','motor_pos1','speed1','ID2','motor_pos2','speed2']
  #  global filename
    #count = 0
    global count
    #time.sleep(0.1)
   # print("motor1:",dxl_present_position,"motor2:",dxl_present_position1,"motor3:",dxl_present_position2)
    with open(filename, 'a') as csvfile:
         
        a =[{'ID':str(ID),'motor_pos':str(dxl_present_position),'speed':str(readspeed(1,2,3)[0]),'ID1':str(ID1),'motor_pos1':str(dxl_present_position1),'speed1':str(readspeed(1,2,3)[1]),'ID2':str(ID2),'motor_pos2':str(dxl_present_position2),'speed2':str(readspeed(1,2,3)[2])}]
        writer = csv.DictWriter(csvfile, fieldnames= fields)
       # writer.writeheader()
        writer.writerows(a)
       # print(a,count)
        #remove this 100 count
        if count > 100:
            csvfile.close()
            return 1
    count+=1
    

       
def readfile():
    
    with open(filename, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter =',')
        temp = next(readCSV)
        D1 = int(temp[1])
        D3 = int(temp[4])
        D5 = int(temp[7])
        
        # set initial speed
        ChangeSpeed_AX(3,20)
        ChangeSpeed_MX(2,20)
        ChangeSpeed_MX(1,20)
        # wait for the motors to reach the first goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, 1, ADDR_MX_GOAL_POSITION, D1)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, 2, ADDR_MX_GOAL_POSITION, D3)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, 3, ADDR_MX_GOAL_POSITION, D5)
        # check that they reached
        check_position_reached(D1 ,D3 ,D5)
        
        for row in readCSV:
            # print(row[1])
            
            time1 = time.time()
            DXL_ID = row[0]
            DXL_ID1 = row[3]
            DXL_ID2 = row[6]
       # row[1] = goal_pos
            D2 = int(row[1])
            D4 = int(row[4])
            D6 = int(row[7])
            speed = calculating_speed(D2,D1)[0]
            speed1 = calculating_speed(D4,D3)[0]
            speed2 = calculating_speed(D6,D5)[1]
            if speed == '0':
                speed = '1'
            elif speed1 == '0':
                speed1 = '1'
            elif speed2 == '0':
                speed2 = '1'

            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num,int(DXL_ID), 32, int(speed))
            dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(port_num,int(DXL_ID1), 32, int(speed1))
            dxl_comm_result2, dxl_error2 = packetHandler.write2ByteTxRx(port_num,int(DXL_ID2), 32, int(speed2))
            #print("Speed is set")
            #dxl_present_speed, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num,int(DXL_ID), 32)
            #time.sleep(0.2)
            #print(dxl_present_speed)
            
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, int(DXL_ID), ADDR_MX_GOAL_POSITION, D2)
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, int(DXL_ID1), ADDR_MX_GOAL_POSITION, D4)
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, int(DXL_ID2), ADDR_MX_GOAL_POSITION, D6)
            if dxl_comm_result != COMM_SUCCESS:
                print("THIS IS THE PROBLEM 1")
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
                print("THIS IS THE PROBLEM 2")
            else:
                D1=D2
                D3=D4
                D5=D6
                delaytime = time.time() - time1            
                time.sleep(sampling_rate - delaytime)
                print("readfile",delaytime)
                #print("time is",time.time()-time1)
                #print(int(speed))
                
            #else:
                #check_position_reached(int(goal_pos))
                
def calculating_speed(new_pos,old_pos):
    speed = abs(((((new_pos - old_pos)*0.08791)/360)/sampling_rate)/0.0019)
    speed1 = abs(((((new_pos - old_pos)*0.29)/300)/sampling_rate)/0.00185)
    return speed, speed1   
        
      
        
    

def home_config(goal_Pos1,goal_Pos2,goal_Pos3):
    DXL_ID = [1,2,3]
    dxl_comm_result1, dxl_error1 = packetHandler.write2ByteTxRx(port_num, DXL_ID[0], ADDR_MX_GOAL_POSITION, goal_Pos1)
    if dxl_comm_result1!= COMM_SUCCESS:
        print("THIS IS THE PROBLEM 1")
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result1))
    elif dxl_error1 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error1))
        print("THIS IS THE PROBLEM 2")
    else:
        print("THIS IS OK!")
    time.sleep(0.2)
    "reading the present position and stopping if threshold is lower than 20"
    dxl_present_position1, dxl_comm_result1, dxl_error1 = packetHandler.read2ByteTxRx(port_num, DXL_ID[0], ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result1 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result1))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error1))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[0], goal_Pos1, dxl_present_position1))

        if not abs(goal_Pos1 - dxl_present_position1) > DXL_MOVING_STATUS_THRESHOLD:
            return
    else:
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[0], goal_Pos1, dxl_present_position1))

    dxl_comm_result2, dxl_error2 = packetHandler.write2ByteTxRx(port_num, DXL_ID[1], ADDR_MX_GOAL_POSITION, goal_Pos2)
    if dxl_comm_result2!= COMM_SUCCESS:
        print("THIS IS THE PROBLEM 1")
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result2))
    elif dxl_error2 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error2))
        print("THIS IS THE PROBLEM 2")
    else:
        print("THIS IS OK!")
    time.sleep(0.2)
    "reading the present position and stopping if threshold is lower than 20"
    dxl_present_position2, dxl_comm_result2, dxl_error2 = packetHandler.read2ByteTxRx(port_num, DXL_ID[1], ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result2 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result2))
    elif dxl_error2 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error2))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[1], goal_Pos2, dxl_present_position2))

        if not abs(goal_Pos2 - dxl_present_position2) > DXL_MOVING_STATUS_THRESHOLD:
            return
    else:
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[1], goal_Pos2, dxl_present_position2))

    dxl_comm_result3, dxl_error3 = packetHandler.write2ByteTxRx(port_num, DXL_ID[2], ADDR_MX_GOAL_POSITION, goal_Pos3)
    if dxl_comm_result3 != COMM_SUCCESS:
        print("THIS IS THE PROBLEM 1")
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result3))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error3))
        print("THIS IS THE PROBLEM 2")
    else:
        print("THIS IS OK!")
    time.sleep(0.2)
    "reading the present position and stopping if threshold is lower than 20"
    dxl_present_position3, dxl_comm_result3, dxl_error3 = packetHandler.read2ByteTxRx(port_num, DXL_ID[2], ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result3 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result3))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error3))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[2], goal_Pos3, dxl_present_position3))

        if not abs(goal_Pos3 - dxl_present_position3) > DXL_MOVING_STATUS_THRESHOLD:
            return
    else:
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID[2], goal_Pos3, dxl_present_position3))


def read(DXL1_ID,DXL2_ID):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, DXL1_ID, ADDR_MX_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % DXL1_ID)

    # Enable Dynamixel#1 Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, DXL2_ID, ADDR_MX_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % DXL2_ID)

    # Add parameter storage for Dynamixel#1 present position
    dxl_addparam_result = groupBulkRead.addParam(DXL1_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkRead addparam failed" % DXL1_ID)
        quit()

    # Add parameter storage for Dynamixel#2 moving value
    dxl_addparam_result = groupBulkRead.addParam(DXL2_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkRead addparam failed" % DXL2_ID)
        quit()
        
    while 1:
        # Bulkread present position and moving status
        dxl_comm_result = groupBulkRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupbulkread data of Dynamixel#1 is available
        dxl_getdata_result = groupBulkRead.isAvailable(DXL1_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % DXL1_ID)
            quit()

        # Check if groupbulkread data of Dynamixel#2 is available
        dxl_getdata_result = groupBulkRead.isAvailable(DXL2_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % DXL2_ID)
            quit()

        # Get Dynamixel#1 present position value
        dxl1_present_position = groupBulkRead.getData(DXL1_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)

        # Get Dynamixel#2 moving value
        dxl2_present_position = groupBulkRead.getData(DXL2_ID, ADDR_MX_PRESENT_POSITION, LEN_MX_PRESENT_POSITION)
        print("[ID:%03d] Present Position : %d \t [ID:%03d] Present Position: %d " % (DXL1_ID, dxl1_present_position, DXL2_ID, dxl2_present_position))
#         dict = {"ID2" : dxl2_present_position}
#         dict['ID2']


def check_position_reached(goal_Pos ,goal_Pos1 ,goal_Pos2):
    
    while 1:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, 1, ADDR_MX_PRESENT_POSITION)
        dxl_present_position1, dxl_comm_result1, dxl_error1 = packetHandler.read2ByteTxRx(port_num, 2, ADDR_MX_PRESENT_POSITION)
        dxl_present_position2, dxl_comm_result2, dxl_error2 = packetHandler.read2ByteTxRx(port_num, 3, ADDR_MX_PRESENT_POSITION)

        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
            
            
            #print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, goal_Pos, dxl_present_position))
        else:
            print("this is running")
            if not (check_threshold(goal_Pos, dxl_present_position) and check_threshold(goal_Pos1, dxl_present_position1) and check_threshold(goal_Pos2, dxl_present_position2)):
                break

def check_threshold(goal_Pos, dxl_present_position):
    return abs(goal_Pos - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD
    
def ChangeSpeed_AX(DXL_ID,speed):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num,DXL_ID, 32, speed)
    print("Speed is set")
    dxl_present_speed, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, DXL_ID, 32)
    time.sleep(0.2)
    print(dxl_present_speed)

def ChangeSpeed_MX(DXL_ID,speed):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num,DXL_ID, 32, speed)
    print("Speed is set")
    dxl_present_speed, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, DXL_ID, 32)
    time.sleep(0.2)
    print(dxl_present_speed)    