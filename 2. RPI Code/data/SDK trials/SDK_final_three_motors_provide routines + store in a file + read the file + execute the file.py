import os
import csv
#import pandas as pd
from bluetooth import *
import time
from dynamixel_sdk import *
#import dynamixel_functions as dynamixel

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
    
data = '' 
server_socket = BluetoothSocket(RFCOMM)
port = 1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print ("Accepted connection from ",address)


ADDR_MX_TORQUE_ENABLE = 24  # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36
LEN_MX_PRESENT_POSITION     = 2
count = 0


# Protocol version
PROTOCOL_VERSION = 1.0  # See which protocol version is used in the Dynamixel

# Default setting
# Dynamixel ID : 1
BAUDRATE = 1000000  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'  # Check which port is being used on your controller                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque

DXL_MOVING_STATUS_THRESHOLD = 5  # Dynamixel moving status threshold
port_num = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
COMM_SUCCESS = 0
COMM_TX_FAIL = -1001
filename = "routines.csv"

groupBulkRead = GroupBulkRead(port_num, packetHandler)

"Opening the port and setting the baudrate"
if port_num.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()
# Set port baudrate
if port_num.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()
"just to check the connection"
DXL_ID = [1,2,3]

"enabling the torque and checking if dynamixel is connected"
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, DXL_ID[0], ADDR_MX_TORQUE_ENABLE, 0)  # TORQUE_DISABLE
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")



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


def read_ax(id3):
    open(filename, 'w').close()
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, id3, ADDR_MX_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % id3)

    while 1:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, id3, ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            #print("[ID:%03d] PresPos:%03d" % (id3, dxl_present_position))
            #dxl_present_position = a
            
            if writefile(id3,dxl_present_position) == 1:
                
                break
            
def readspeed(id3):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, id3, ADDR_MX_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % id3)

    while 1:
        dxl_speed, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num, id3, 38)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            return 6000
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
            return 6000
        else:
            print("[ID:%03d] Speed:%03d" % (id3, dxl_speed))
            return dxl_speed
        

def writefile(id3,dxl_present_position):
    fields = ['ID','motor_pos','speed']
  #  global filename
  #  count = 0
    global count
    #time.sleep(0.1)
    
    with open(filename, 'a') as csvfile:
        
        a =[{'ID':str(id3),'motor_pos':str(dxl_present_position),'speed':str(readspeed(id3))}]
        writer = csv.DictWriter(csvfile, fieldnames= fields)
       # writer.writeheader()
        writer.writerows(a)
        print(a,count)
        if count > 100:
            csvfile.close()
            return 1
    count+=1
    

       
def readfile():
    with open(filename, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter =',')
        for row in readCSV:
            # print(row[1])
            DXL_ID = row[0] 
       # row[1] = goal_pos
            speed = row[2]  
            goal_pos = row[1] 
            if speed == '0':
                speed = '1'
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num,int(DXL_ID), 32, int(speed))
            print("Speed is set")
            dxl_present_speed, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(port_num,int(DXL_ID), 32)
            #time.sleep(0.2)
            print(dxl_present_speed)
            
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(port_num, int(DXL_ID), ADDR_MX_GOAL_POSITION, int(goal_pos))
            if dxl_comm_result != COMM_SUCCESS:
                print("THIS IS THE PROBLEM 1")
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
                print("THIS IS THE PROBLEM 2")

        
        
      
        
    

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



#readspeed(2)
read_ax(2)
readfile()
#store_readings(1,2,3)
#check_data_position(1,2,3)
#read_presentPositions(1,2,3)
ChangeSpeed_AX(3,20)
ChangeSpeed_MX(2,100)
ChangeSpeed_MX(1,20)
#value1 =
#value2 = 1023
#value3 = 
#home_config(value1, value2, value3)
while True:
    data += client_socket.recv(1024).decode("utf-8")
    if data[-1] == '\n':
        print(data)
        info = data.split(',')
        data = ''
    
    "home configuration - on pressing reset"
    
    if info[0] == "r":
        value1 = 1023
        value2 = 1023
        value3 = 200
        home_config(value1,value2,value3)
        
    if info[0] == "1":
        angle1 = int((2047*int(info[1]))/180)
        move_motor(angle1)
        

    if info[0] == "2":
        angle2 = int((2047*int(info[1]))/180)
        move_motor(angle2)

    if info[0] == "3":
        angle3 = int((512*int(info[1]))/150)
        move_motor(angle3)
    
    if info[0] == "s":
        read_ax(3)



groupBulkRead.clearParam()
port_num.closePort()
client_socket.close()
server_socket.close()


