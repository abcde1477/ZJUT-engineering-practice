# 灯光代码
from time import sleep
from Rosmaster_Lib import Rosmaster

bot = Rosmaster()


def light():
    i = 0
    for i in range(100):
        # bot.set_colorful_lamps(i,0,0,0)
        bot.set_colorful_lamps(i, 255, 255, 255)


def turn_off_lights():
    for i in range(100):
        bot.set_colorful_lamps(i, 0, 0, 0)


def light_meet_obstacle():  # 遇见障碍（红灯）
    on_time = 1000
    bot.set_beep(on_time)
    for i in range(500):
        bot.set_colorful_lamps(i, 255, 0, 0)
    turn_off_lights()
    turn_off_lights()


def light_unreachable_start():  # 不可达
    for i in range(500):
        bot.set_colorful_lamps(i, 255, 0, 0)
    on_time = 250
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(0.5)


def light_unreachable_over():
    turn_off_lights()
    turn_off_lights()


def light_on_load_start():  # 在路上
    bot.set_colorful_effect(3, 6, parm=3)  # 呼吸灯（黄灯）
    # sleep(5)


def light_on_load_over():
    bot.set_colorful_effect(0, 1)  # 关
    turn_off_lights()


def light_get_goal():  # 到达货物点
    bot.set_colorful_effect(4, 6, parm=1)  # 渐变灯
    on_time = 250
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(0.5)
    bot.set_beep(on_time)
    sleep(1.5)
    bot.set_colorful_effect(0, 1)  # 关



def light_go_back_start():  # 回到起点
    bot.set_colorful_effect(1, 6, parm=1)  # 流水灯


def light_go_back_over():
    bot.set_colorful_effect(0, 1)  # 关
    turn_off_lights()


if __name__ == '__main__':
    bot.set_colorful_effect(0, 1)
    print("meet_obstacle")
    light_meet_obstacle()

    sleep(1)

    print("unreachable_start")
    light_unreachable_start()
    sleep(3)
    light_unreachable_over()

    sleep(1)

    print("on_load_start")
    light_on_load_start()
    sleep(3)
    light_on_load_over()

    sleep(1)

    print("get_goal")
    light_get_goal()

    sleep(1)

    print("go_back_start")
    light_go_back_start()
    sleep(3)
    light_go_back_over()

    # i = 0
# while 1:
# light()
# sleep(5)
# turn_off_lights()
# bot.set_colorful_effect(1, 6, parm=1)#流水灯
# sleep(5)
# turn_off_lights()
# bot.set_colorful_effect(4, 6, parm=1)#渐变灯
# sleep(5)
# turn_off_lights()
# bot.set_colorful_effect(3, 6, parm=1)#呼吸灯
# sleep(5)
# turn_off_lights()
# for i in range(100):
#   bot.set_colorful_lamps(i,0,0,0)
#   bot.set_colorful_lamps(i,255,255,255)
# bot.set_colorful_lamps(1,255,255,255)
# bot.set_colorful_lamps(3,255,255,255)
# bot.set_colorful_lamps(2,255,255,255)
# bot.set_colorful_lamps(4,255,255,255)
# bot.set_colorful_lamps(5,255,255,255)
# bot.set_colorful_lamps(6,255,255,255)
# bot.set_colorful_lamps(7,255,255,255)