import os
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
    
    
server_socket = BluetoothSocket(RFCOMM)
port = 1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print ("Accepted connection from ",address)


ADDR_MX_TORQUE_ENABLE = 24  # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36

# Protocol version
PROTOCOL_VERSION = 1.0  # See which protocol version is used in the Dynamixel

# Default setting
# Dynamixel ID : 1
BAUDRATE = 57600  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'  # Check which port is being used on your controller                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque

DXL_MOVING_STATUS_THRESHOLD = 5  # Dynamixel moving status threshold
port_num = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
COMM_SUCCESS = 0
COMM_TX_FAIL = -1001
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
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_num, DXL_ID[0], ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)  # TORQUE_DISABLE
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


ChangeSpeed_AX(3,20)
ChangeSpeed_MX(2,20)
ChangeSpeed_MX(1,20)
while True:
    data += client_socket.recv(1024).decode("utf-8")
    if data[-1] == '\n':
        print(data)
        info = data.split(',')
        data = ''
    
    
    if info[0] == "1":
        angle1 = int((2047*int(info[1]))/180)
        move_motor(angle1)
        

    if info[0] == "2":
        angle2 = int((2047*int(info[1]))/180)
        move_motor(angle2)

    if info[0] == "3":
        angle3 = int((512*int(info[1]))/150)
        move_motor(angle3)




port_num.closePort()
client_socket.close()
server_socket.close()


