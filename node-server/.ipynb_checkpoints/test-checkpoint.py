import requests


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

        self.test_counter = 0
        self.obstacle_clear_test_counter = 0

    def get_task(self):
        use = 0
        if use == 0:
            response = requests.get(self.get_task_url)
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print("JSON Response:", json_data)

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
                    "from": (6, 0),
                    "description": "前往A2货柜取货"
                }
            elif self.test_counter % 3 == 1:
                return {
                    "task_id": 321,
                    "task_type": "fetch",
                    "from": (4, 8),
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
                    "from": (6, 0),
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
        i, j = location
        post_url = f"{self.post_car_location_url}/{i}/{j}" 
        response = requests.put(self.post_car_location_url)
        if response.status_code == 200:
            print("post car location succeed")
        else:
            print("Fail in post message")

    def post_obstacle(self, location):
        # 报告障碍物位置
        # location可元组可列表

        i, j = location
        post_url = f"{self.post_obstacle_url}/{i}/{j}"  
        response = requests.post(self.post_obstacle_url)
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
            #{
            # "obstacle_clear":"yes"
            #}
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
            self.obstacle_clear_test_counter += 1
            if self.obstacle_clear_test_counter > 10 == 0:
                return True
            else:
                return False


if __name__ == '__main__':
    "192.168.109.127"
    server = NetworkInteract("http://192.168.109.127:3000")
    # 测试

    print("小车发送地图")
    input()
    server.send_map(
        [
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
    )
    print()

    # 报告小车位置
    print("报告小车位置")
    input()
    server.report_car_location((0,0))
    print()

    # 请求任务
    print("请求任务")
    input()
    print("任务是:"+str(server.get_task()))
    print()

    # 多次报告小车位置
    print("多次报告小车位置")
    i = 0
    while i < 3:
        input()
        server.report_car_location((i, 0))
        i += 1
    print()

    # 报告障碍物品1
    print("报告障碍物品")
    input()
    server.post_obstacle((3,0))
    print()


    # 报告障碍物品2
    print("报告障碍物品")
    input()
    server.post_obstacle((2,1))
    print()


    # 报告不可达
    print("向"+str(server.post_unreachable_url)+"报告不可达")
    input()
    server.post_unreachable()
    print()


    # 反复询问是否清除障碍
    print("向:"+server.query_is_obstacle_clear_url+"反复询问是否清除障碍")
    input()
    while True:
        reachable=server.get_is_obstacle_clear()
        print("是否清除:"+str(reachable))
        if reachable:
            break
        input()
    print()


    # 多次报告小车位置
    print("多次报告小车位置")
    i = 0
    while i < 3:
        input()
        server.report_car_location((i,0))
        i += 1
    print()


