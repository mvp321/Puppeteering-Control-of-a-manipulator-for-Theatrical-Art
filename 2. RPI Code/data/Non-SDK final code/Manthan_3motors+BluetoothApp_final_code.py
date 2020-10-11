from bluetooth import *
from pyax12.connection import Connection
import time
#esthablishing serial communication
serial_connection = Connection(port="/dev/ttyUSB1", baudrate=57600)
dynamixel_id1 = 1
#mx64 motor id = 2
dynamixel_id2 = 2
#ax12 motor id = 3
dynamixel_id3 = 3

#speed variables for all the motors, change if required
speed1=20
speed2=20
speed3=20
mainspeed=20

server_socket = BluetoothSocket( RFCOMM )

port = 1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print ("Accepted connection from "),address

data = ''
while True:
    data += client_socket.recv(1024).decode("utf-8") 
    if data[-1] == '\n':
        info = data[0:len(data)-1].split(',')
        print(info)
        #print("Motor ID", info[0])
        #print("Angle", info[1])
        #info = ''
        #ata = ''
        
        if info[0]=="1":
           # print("The infor is ", int(info[1]))
            Angle1=595-((int(info[1]))*3.333)
            #print("The angle is ", Angle1)
            #0AngleInfo=595data, 180AngleInfo=-5data
            #1AngleInfo=3.333
            #AngleData=595-((info[1])*3.333)
            #MX28 Limits
            if Angle1<-60:
               A1=-60
            elif Angle1>680:
               A1=680
            else:
               A1 = Angle1             
            serial_connection.goto(dynamixel_id1, A1, speed=speed1, degrees=True)


        elif info[0]=="2":
            Angle2=540-((int(info[1])-9)*3.312)
            #9AngleInfo=540data, 163AngleInfo=30data
            #1AngleInfo=3.312
            #AngleData=540-((info[1]-9)*3.312)
            #MX64 Limits
            if Angle2<30:
               A2=30
            elif Angle2>540:
               A2=540
            else:
               A2 = Angle2             
            serial_connection.goto(dynamixel_id2, A2, speed=speed2, degrees=True)
            
            
        elif info[0]=="3":
            Angle3=int(info[1])-90
            #input value will be between 0 to 180, eg, info 180 = 90 in data
            #1data=1AngleInfo
            #AX12 Limits
            if Angle3<-90:
               A3=-90
            elif Angle3>90:
               A3=90
            else:
               A3 = Angle3             
            serial_connection.goto(dynamixel_id3, A3, speed=speed3, degrees=True)

    # HomeConfiguration
    serial_connection.goto(dynamixel_id1, 300, speed=speed1, degrees=True)
    serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
    serial_connection.goto(dynamixel_id3, 0, speed=speed3, degrees=True)

    # YesMotionFunction
    serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)
    serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
    serial_connection.goto(dynamixel_id2, 180, speed=speed2, degrees=True)
    serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)

    # NoMotionFuntion
    serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
    serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)
    serial_connection.goto(dynamixel_id1, 500, speed=speed1, degrees=True)
    serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)


#        serial_connection.goto(int(info[0]), int(info[1]), speed=mainspeed, degrees=True)
#     info = ''
    data = ''
            

serial_connection.close()
client_socket.close()
server_socket.close()