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
speed1=80
speed2=50
speed3=80

Angle1=40 #ranging from 40 to 680, positive towards anticlockwise when viewing from the top
Angle2=30 #ranging from 30 t0 280, positive towards downwards when looking from any direction
Angle3=90 #ranging from -90 to 90, positive towards upside


#MX28 Limits
if Angle1<40:
    A1=40
elif Angle1>680:
    A1=680
else:
    A1 = Angle1

#MX64 Limits
if Angle2<30:
    A2=30
elif Angle2>280:
    A2=280
else:
    A2 = Angle2


#AX12 Limits
if Angle3<-90:
    A3=-90
elif Angle3>90:
    A3=90
else:
    A3 = Angle3


# MX28
serial_connection.goto(dynamixel_id1, A1, speed=speed1, degrees=True)
#time.sleep(1)

# MX64
serial_connection.goto(dynamixel_id2, A2, speed=speed2, degrees=True)
#time.sleep(1)

# AX12
serial_connection.goto(dynamixel_id3, A3, speed=speed3, degrees=True)
time.sleep(3)


#HomeConfiguration
serial_connection.goto(dynamixel_id1, 300, speed=speed1, degrees=True)
serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
serial_connection.goto(dynamixel_id3, 0, speed=speed3, degrees=True)

#YesMotionFunction
serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)
serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
serial_connection.goto(dynamixel_id2, 180, speed=speed2, degrees=True)
serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)

#NoMotionFuntion
serial_connection.goto(dynamixel_id2, 30, speed=speed2, degrees=True)
serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)
serial_connection.goto(dynamixel_id1, 500, speed=speed1, degrees=True)
serial_connection.goto(dynamixel_id1, 200, speed=speed1, degrees=True)


# Close the serial connection
serial_connection.close()