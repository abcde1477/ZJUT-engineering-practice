import time
import rospy
from Rosmaster_Lib import Rosmaster

from cali import *



##

pid = PIDController(Kp=0.20, Ki=0.0, Kd=0.0)



drive_imported = True


# #矫正
goTime = 1.00
goSpeed = 0.42
turnSpeed =1.6
turnTime = 1.65
# #

def turn_left_motor(bot,use_cali):
    st  = time.time()
    bot.set_car_motion(0,0,turnSpeed)
    while time.time()-st<turnTime:
        a =1
    bot.set_car_motion(0,0,0)

    if use_cali:
        cali_line(cap, pid, bot)



def turn_right_motor(bot,use_cali):
    st  = time.time()
    bot.set_car_motion(0,0,-turnSpeed)
    while time.time()-st<turnTime:
        a =1
    bot.set_car_motion(0,0,0)

    if use_cali:
        cali_line(cap, pid, bot)
    

def go_forward(bot,use_cali):
    st  = time.time()
    bot.set_car_motion(goSpeed,0,0)
    while time.time()-st<goTime: # 3
        a =1
    bot.set_car_motion(0,0,0)

    if use_cali:
        cali_line(cap, pid, bot)


def go_back_motor(bot,use_cali):
    st  = time.time()
    bot.set_car_motion(-goSpeed,0,0)
    while time.time()-st<goTime: # 3
        a =1
    bot.set_car_motion(0,0,0)

    if use_cali:
        cali_line(cap, pid, bot)



if __name__ == '__main__':
    bot = Rosmaster()
    # go_forward(bot)
    # cali_line(cap, pid, bot)
    # go_forward(bot,False)
    turn_left_motor(bot,True)
    cap.release()
    del bot
    



