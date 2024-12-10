from web import run_flask, start_websocket_server, squares, colors, flagz
import asyncio
import threading
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from clover import srv
from std_srvs.srv import Trigger
import math
from sensor_msgs.msg import Range
from random import randint
from mavros_msgs.srv import CommandBool, CommandLong
from pymavlink import mavutil
from std_msgs.msg import String

rospy.init_node('cv')

bridge = CvBridge()

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_altitude = rospy.ServiceProxy('set_altitude', srv.SetAltitude)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
send_command = rospy.ServiceProxy('mavros/cmd/command', CommandLong)
topic = rospy.Publisher('/buildings', String, queue_size=1)

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x**2 + telem.y**2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def run_main():
    while not flagz[0]:
        rospy.sleep(1)
    
    navigate(x=0, y=0, z=1.8, frame_id='body', auto_arm=True)
    rospy.sleep(10)
    for Y in range(10):
        for X in range(10):
            while flagz[3]:
                rospy.sleep(0.1)
            if Y % 2 :
                X = 9-X
            navigate(x=X, y=Y, z=1.8, frame_id='aruco_map')
            rospy.sleep(3)
            # print(X,Y)

            dist = rospy.wait_for_message('rangefinder/range', Range).range
            if dist < 1.2:
                rospy.sleep(2)
                img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                b_mask = cv2.inRange(hsv, (120, 100, 100), (120, 255, 255))
                g_mask = cv2.inRange(hsv, (39, 100, 100), (78, 255, 255))
                y_mask = cv2.inRange(hsv, (25, 100, 100), (30, 255, 255))
                r_mask = cv2.inRange(hsv, (0, 100, 100), (5, 255, 255))

                b_num = cv2.countNonZero(b_mask)
                g_num = cv2.countNonZero(g_mask)
                y_num = cv2.countNonZero(y_mask)
                r_num = cv2.countNonZero(r_mask)

                if b_num > r_num and b_num > y_num and b_num > g_num and b_num > 500:
                    print('blue')
                    color123 = 'blue'
                elif y_num > r_num and y_num > b_num and y_num > g_num and y_num > 500:
                    print('yellow')
                    color123 = 'yellow'
                elif g_num > r_num and g_num > b_num and g_num > y_num and g_num > 500:
                    print('green')
                    color123 = 'green'
                elif r_num > g_num and r_num > y_num and r_num > b_num and r_num > 500:
                    print('red') 
                    color123 = 'red'
                else:
                    print('non')
                    color123 = 'non'
                print(X,Y)
                coordx = X*60
                coordy = Y*60
                squares.append({"x": coordx, "y": coordy, "color": color123})
            
    navigate_wait(x=0, y=0, z=2, speed = 3,frame_id='aruco_map')
    rospy.sleep(4)
    land()
    str_result = ''  
    for i, square in enumerate(squares):
        arr = list(square.values())
        str_result += f'{i+1} in ({arr[0] // 60}, {arr[1] // 60}) with color {arr[2]}; '
    topic.publish(data=str_result)

def check_flagz():
    while True:
        rospy.sleep(0.5)
        if flagz[1]:
            land()
        elif flagz[2]:
            send_command(command=mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=0, param2=21196)


flask_task = threading.Thread(target=run_flask)
flask_task.start()
print('.')
check_task = threading.Thread(target=check_flagz)
check_task.start()

main_task = threading.Thread(target=run_main)
main_task.start()
asyncio.run(start_websocket_server())