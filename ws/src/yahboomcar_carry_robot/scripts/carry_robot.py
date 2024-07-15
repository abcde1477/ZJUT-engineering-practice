# !/usr/bin/env python
# coding:utf-8
import copy
import requests
import time

from DoubleBFS import get_path_using_DBFS

# from QR import *


# 开关
real_move = True
real_light_buzzer = True
real_laser = True

#
bot = None
if real_move or real_light_buzzer:
    from Rosmaster_Lib import Rosmaster

    bot = Rosmaster()

if real_move:
    from drive import *

if real_light_buzzer:
    from light_buzzer import *

if real_laser:
    from std_msgs.msg import String

move_dist = 3

DirectionUP = [-1, 0]
DirectionLEFT = [0, -1]
DirectionDOWN = [1, 0]
DirectionRIGHT = [0, 1]


def _get_left_direction_of(direction):
    if direction == DirectionUP:
        return DirectionLEFT
    elif direction == DirectionLEFT:
        return DirectionDOWN
    elif direction == DirectionDOWN:
        return DirectionRIGHT
    elif direction == DirectionRIGHT:
        return DirectionUP


def _get_right_direction_of(direction):
    if direction == DirectionUP:
        return DirectionRIGHT
    elif direction == DirectionRIGHT:
        return DirectionDOWN
    elif direction == DirectionDOWN:
        return DirectionLEFT
    elif direction == DirectionLEFT:
        return DirectionUP


def _get_back_direction_of(direction):
    if direction == DirectionUP:
        return DirectionDOWN
    if direction == DirectionLEFT:
        return DirectionRIGHT
    if direction == DirectionDOWN:
        return DirectionUP
    if direction == DirectionRIGHT:
        return DirectionLEFT


class ObstacleLaser:
    def __init__(self):
        self.laser = rospy.init_node('laser_reader', anonymous=False)

    def get_nearby(self):
        nearby_message = rospy.wait_for_message('/obstacle_message', String).data
        left_has_obstacle = int(nearby_message[0]) == 1
        front_has_obstacle = int(nearby_message[1]) == 1
        right_has_obstacle = int(nearby_message[2]) == 1

        return [left_has_obstacle, front_has_obstacle, right_has_obstacle]

    def quit(self):
        self.laser.unregister()


class Car:
    def __init__(self, bot, the_map, initial_location, initial_direction):
        # 获取引用
        self.bot = bot
        self.map = the_map  # python中传入的数组是引用！，这里改变，外部的会改变
        self.location = initial_location
        self.direction = initial_direction
        if real_laser:
            self.obstacle_laser = ObstacleLaser()
        # 测试
        # self.map[3][4] = 1
        # print("self.map")
        # print(self.map)
        self.orderList = []

    def _get_nearby_obstacle(self):
        use = 0  # 选择器

        if real_laser:
            use = 0
        else:
            use = 1

        # 无雷达选择测试数据
        if use == 0:
            pass
            # 雷达实现后：
            return self.obstacle_laser.get_nearby()
        elif use == 1:
            # 雷达未实现，测试数据
            if self.location == [4, 2]:
                if self.direction == DirectionRIGHT:
                    return [True, True, True]
            elif self.location == [2, 2]:
                if self.direction == DirectionRIGHT:
                    return [True, True, True]
            return [False, False, False]
        elif use == 2:
            return [False, False, False]

    def turn_left(self,left_no_wall):
        # 更变自身属性

        self.direction = _get_left_direction_of(self.direction)

        print("左转")
        self.orderList.append("左转")
        # self._turn_left_motor()

        # fix：如果转后是障碍物就不循线
        left_no_obstacle = self._get_nearby_obstacle()[0] == False
        if left_no_wall and left_no_obstacle:
            use_cali=True
        else:
            use_cali=False

        if real_move:
            turn_left_motor(bot, use_cali)
        pass  # 左应旋转指令

    def turn_right(self,right_no_wall):
        # 更变自身属性
        self.direction = _get_right_direction_of(self.direction)
        print("右转")
        self.orderList.append("右转")

        right_no_obstacle = self._get_nearby_obstacle()[2] == False
        if right_no_wall and right_no_obstacle:
            use_cali=True
        else:
            use_cali=False

        if real_move:
            turn_right_motor(bot,use_cali)
        pass  # 右旋转指令

    def go_ahead(self,right_no_wall):
        self.location[0] += self.direction[0]
        self.location[1] += self.direction[1]
        print("前进")

        self.orderList.append("前进")

        front_no_obstacle = self._get_nearby_obstacle()[1] == False
        if real_move:
            go_forward(bot,front_no_obstacle)
        pass  # 前进指令

    def _move(self, direction,next_location):

        # 中断: 前往的方向有障碍->将障碍物添加到网格中。重新计算生成路径 return False
        #
        # return False

        left_obstacle_flag, front_obstacle_flag, right_obstacle_flag = self._get_nearby_obstacle()

        print(f"当前方向: {self.direction}")

        left_direction = _get_left_direction_of(self.direction)
        right_direction = _get_right_direction_of(self.direction)
        back_direction = _get_back_direction_of(self.direction)
        is_next_location_no_wall = self.map[next_location[0]][next_location[1]] == 0

        # 检测障碍再转向
        if left_direction == direction:  # 左
            if left_obstacle_flag:
                # 中断
                return False
            self.turn_left(is_next_location_no_wall)
            self.go_ahead(True)
        elif right_direction == direction:  # 右
            if left_obstacle_flag:
                # 中断
                return False
            self.turn_right(is_next_location_no_wall)
            self.go_ahead(True)
        elif back_direction == direction:  # 后
            self.turn_right(is_next_location_no_wall)
            self.turn_right(is_next_location_no_wall)
            self.go_ahead(True)
        else:  # 前
            if front_obstacle_flag:
                # 中断
                return False
            self.go_ahead(True)
        print()
        return True

    def get_list(self):
        # 指令序列
        return self.orderList

    def clearOrderList(self):
        self.orderList = []

    def get_location(self):
        return self.location

    def get_map(self):
        return self.map

    def go_to_location(self, next_location):

        x = next_location[0] - self.location[0]
        y = next_location[1] - self.location[1]

        # [x,y]是前往下一位置的方向
        print(f"应走方向:[{x}, {y}]")

        if x == 0 and y == 0:
            print("不走")
            return None
        # next_location用来检测墙/障碍物
        if self._move([x, y],next_location):
            # _move返回true为成功
            print("走")
            # 发送一次自身位置数据:

            self.location[0] = next_location[0]
            self.location[1] = next_location[1]
        else:
            # _move返回false为此操作会撞障碍物
            return next_location  # 返回障碍物坐标


# car control status


class CarControl:
    def __init__(self):
        self.return_location = (0, 0)
        # task的形式1：
        # {
        # "task_id": 321
        # "task_type": "fetch"
        # "from": ()
        # "finalDirection": (4，5)
        # "description":"前往A2货柜取货"

        # -------------------

        # task的形式2：
        # {
        # "task_id": 322
        # "task_type": "directlyControl"
        # "turn" : "LEFT" 或"RIGHT"
        # "go_ahead" :2
        # "description":"左转，前进2"
        # }

        obstacle_map55 = [
            [0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

        obstacle_map99 = [
            [0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0]
        ]
        # self.map是初始地图
        self.map = obstacle_map99
        self.map_copy = copy.deepcopy(self.map)

        self.car = Car(None, self.map_copy, [0, 0], DirectionRIGHT)

        self.network = NetworkInteract("http://localhost:3000")
        self.network.send_map(self.map)

    def _go(self, goal_location):

        print("_go:" + str(goal_location))
        begin = tuple(self.car.get_location())
        goal = tuple(goal_location)
        car_map_ref = self.car.get_map()
        obstacle_clear = True
        while True:
            path = get_path_using_DBFS(car_map_ref, begin, goal)
            if path:
                # 有路径
                pass
            else:
                self.network.post_unreachable()
                light_unreachable_start()
                print("无法到达")
                ## 等待移除障碍物
                while True:
                    # 询问是否移除障碍物
                    time.sleep(2)
                    if self.network.get_is_obstacle_clear():
                        car_map_ref = copy.deepcopy(self.map)
                        light_unreachable_over()
                        if goal == self.return_location:
                            light_go_back_start()
                        else:
                            light_on_load_start()
                        break

                path = get_path_using_DBFS(car_map_ref, begin, goal)

            obstacle_location = None

            # 沿着path一步一步走
            for ele in path:
                # path不会是空
                print(f"将要前往:[{ele[0]}, {ele[1]}]")
                obstacle_location = self.car.go_to_location(ele)
                if obstacle_location:
                    # 障碍物中断
                    # 但不能在for里修改path，所以跳出循环在外部处理
                    self.network.post_obstacle(obstacle_location)
                    light_meet_obstacle()
                    break  # 到if obstacle_location:

                # 走完报告,中断不走，跳出循环所以不报告
                self.network.report_car_location(self.car.get_location())

            if obstacle_location:
                print("出现障碍物")
                # 在obstacle_map上添加障碍物，给状态图设置障碍物，
                if car_map_ref[obstacle_location[0]][obstacle_location[1]] == 1:
                    print("严重错误")
                else:
                    car_map_ref[obstacle_location[0]][obstacle_location[1]] = 1
                print("新obstacle_map")
                print(car_map_ref)
                location_list = self.car.get_location()
                car_location = (location_list[0], location_list[1])  # 转为元组
                begin = car_location
            else:
                break  # 到print(self.car.get_list())
            pass  # while进入下一个循环
        print(self.car.get_list())
        if goal_location == self.car.get_location():
            self.car.clearOrderList()
        # 测试

    def _directlyControl(self, turn, go):
        if turn == "LEFT":
            self.car.turn_left(True)
        if turn == "RIGHT":
            self.car.turn_right(True)
        else:
            pass
        while go != 0:
            self.car.go_ahead(True)
            go -= 1

    def work(self):
        # 从服务器获取任务
        while True:
            task = self.network.get_task()
            if task:
                if task['task_type'] == "fetch":
                    # 取货例程
                    goal = task['from']

                    # 灯光状态设置与指令下发
                    light_on_load_start()
                    self._go(goal)
                    light_on_load_over()

                    # 取到货物
                    light_get_goal()

                    light_go_back_start()
                    self._go(self.return_location)
                    light_go_back_over()


                elif task['task_type'] == "directlyControl":
                    self._directlyControl(task['turn'], task['go_ahead'])

    def build_map(self):
        pass


class NetworkInteract:
    # 与服务器程序的交互
    # 获取任务
    # 发送状态

    # http:192.168.109.127:3000

    def __init__(self, url):
        self.get_task_url = url + "/car/get-task"
        self.post_obstacle_url = url + "/car/add-obstacle-location"
        self.post_map_url = url + "/car/add-map"

        self.post_unreachable_url = url + "/car/unreachable"
        self.query_is_obstacle_clear_url = url + "/car/is-obstacle-cleared"
        self.post_car_location_url = url + "/car/report-location"

        self.test_counter = -1 
        self.obstacle_clear_test_counter = 0

    def get_task(self):
        use = 0
        if use == 0:
            response = requests.get(self.get_task_url)
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print("JSON Response:", json_data)
                    return json_data
                except ValueError:
                    print("Response is not in JSON format")
            elif response.status_code == 204:  # 无任务
                return None

        elif use == 1:
            # 测试数据1
            self.test_counter += 1
            if self.test_counter % 3 == 0:
                return {
                    "task_id": 320,
                    "task_type": "fetch",
                    "from": (4, 4),
                    "description": "前往A2货柜取货"
                }
            elif self.test_counter % 3 == 1:
                return {
                    "task_id": 321,
                    "task_type": "fetch",
                    "from": (3, 0),
                    "description": "前往A2货柜取货"
                }
            elif self.test_counter % 3 == 2:
                return {
                    "task_id": 322,
                    "task_type": "directlyControl",
                    "turn": "LEFT",
                    "go_ahead": 2,
                    "description": "左转，前进2"
                }
        elif use == 2:
            # 测试数据2
            self.test_counter += 1
            if self.test_counter == 1:
                return {
                    "task_id": 320,
                    "task_type": "fetch",
                    "from": (4, 4),
                    "description": "前往A2货柜取货"
                }
            else:
                return None

    def send_map(self, map_ref):
        response = requests.post(self.post_map_url, json=map_ref)

        if response.status_code == 200:
            print("post map succeed")
        else:
            print("Fail in post ")

    def report_car_location(self, location):
        # 报告小车位置
        # location可元组可列表
        i = location[0]
        j = location[1]
        put_url = f"{self.post_car_location_url}/{i}/{j}"

        response = requests.put(put_url)
        if response.status_code == 200:
            print("post car location succeed")
        else:
            print("Fail in post message")

    def post_obstacle(self, location):
        # 报告障碍物位置
        # location可元组可列表

        i = location[0]
        j = location[1]
        post_url = f"{self.post_obstacle_url}/{i}/{j}"
        response = requests.post(post_url)
        if response.status_code == 200:
            print("post obstacle location succeed")
        else:
            print("Fail in post message")

    def post_unreachable(self):
        response = requests.post(self.post_unreachable_url)
        if response.status_code == 200:
            print("post unreachable message succeed")
        else:
            print("Fail in post message")

    def get_is_obstacle_clear(self):

        use = 0
        if use == 0:
            response = requests.get(self.query_is_obstacle_clear_url)
            # {
            # "obstacle_clear":"yes"
            # }
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print("JSON Response:", json_data)
                    if json_data['obstacle_clear'] == "no":
                        return False
                    else:
                        return True
                except ValueError:
                    print("Response is not in JSON format")
        elif use == 1:
            # 测试
            self.obstacle_clear_test_counter += 1
            if self.obstacle_clear_test_counter > 10 == 0:
                return True
            else:
                return False


if __name__ == "__main__":
    carControl = CarControl()
    carControl.work()
    # cap.release()

    # laser = ObstacleLaser()
    # while True:
    #    print(laser.get_nearby())
    # del bot
