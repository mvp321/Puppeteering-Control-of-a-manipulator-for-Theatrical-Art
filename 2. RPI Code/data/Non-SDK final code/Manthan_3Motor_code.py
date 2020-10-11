from pyax12.connection import Connection
import time
#esthablishing serial communication
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)
#mx28 motor id =1 TrunTable
#mx64 motor id = 2 Rotational Joint
#ax12 motor id = 3 Mic

dynamixel_id1 = 1
dynamixel_id2 = 2
dynamixel_id3 = 3

#speed variables for all the motors, change if required
speed1=20
speed2=20
speed3=20

Z1=180 #ranging from 0 to 180
Z2=160 #ranging from 10 to 160
Z3=180 #ranging from 0 to 180


Angle1=595-((Z1)*3.333)
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


Angle2=540-((Z2-9)*3.312)
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
            

Angle3=Z3-90
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


# #HomeConfiguration
# serial_connection.goto(dynamixel_id1, 300, speed=speed1, degrees=True)
# serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
# serial_connection.goto(dynamixel_id3, 0, speed=speed3, degrees=True)
# 
# #YesMotionFunction
# serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)
# serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
# serial_connection.goto(dynamixel_id2, 180, speed=speed2, degrees=True)
# serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
# 
# #NoMotionFuntion
# serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
# serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)
# serial_connection.goto(dynamixel_id1, 500, speed=speed1, degrees=True)
# serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)


# Close the serial connection
serial_connection.close()